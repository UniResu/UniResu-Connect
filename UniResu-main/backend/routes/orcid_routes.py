import contextlib
import os
import secrets
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/api/orcid", tags=["ORCID"])

ORCID_CLIENT_ID       = os.getenv("ORCID_CLIENT_ID",  "APP-MCVYKS2NO8BD3IUZ")
ORCID_CLIENT_SECRET   = os.getenv("ORCID_CLIENT_SECRET", "902a2648-b3d1-494a-9dfd-be9d5a0962d7")
ORCID_REDIRECT_URI    = os.getenv("ORCID_REDIRECT_URI",  "http://127.0.0.1:8000/api/orcid/callback")
ORCID_BASE_URL        = "https://orcid.org"
FRONTEND_REGISTER_URL = "http://127.0.0.1:5500/src/pages/register.html"

_oauth_states: dict = {}


@router.get("/connect")
async def iniciar_orcid():
    state = secrets.token_urlsafe(16)
    _oauth_states[state] = "pendente"
    url = (
        f"{ORCID_BASE_URL}/oauth/authorize"
        f"?client_id={ORCID_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=/authenticate"
        f"&redirect_uri={ORCID_REDIRECT_URI}"
        f"&state={state}"
    )
    return RedirectResponse(url, status_code=302)


@router.get("/callback")
async def orcid_callback(code: str, state: str):
    if state not in _oauth_states:
        raise HTTPException(status_code=400, detail="State invalido ou expirado.")
    del _oauth_states[state]

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            f"{ORCID_BASE_URL}/oauth/token",
            data={
                "client_id":     ORCID_CLIENT_ID,
                "client_secret": ORCID_CLIENT_SECRET,
                "grant_type":    "authorization_code",
                "code":          code,
                "redirect_uri":  ORCID_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Erro ao obter token do ORCID.")

    token_data   = token_resp.json()
    orcid_id     = token_data.get("orcid", "")
    access_token = token_data.get("access_token", "")

    orcid_nome = ""
    async with httpx.AsyncClient() as client:
        perfil_resp = await client.get(
            f"https://pub.orcid.org/v3.0/{orcid_id}/person",
            headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"},
        )

    if perfil_resp.status_code == 200:
        with contextlib.suppress(Exception):
            perfil     = perfil_resp.json()
            nome_obj   = perfil.get("name", {})
            given      = nome_obj.get("given-names", {}).get("value", "")
            family     = nome_obj.get("family-name",  {}).get("value", "")
            orcid_nome = f"{given} {family}".strip()

    redirect_url = (
        f"{FRONTEND_REGISTER_URL}"
        f"?orcid=ok"
        f"&orcid_id={orcid_id}"
        f"&orcid_nome={orcid_nome}"
    )
    return RedirectResponse(redirect_url, status_code=302)