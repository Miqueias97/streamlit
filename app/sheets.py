import gspread as gs
import json, os
from dotenv import load_dotenv
load_dotenv()


urlBase = 'https://docs.google.com/spreadsheets/d/'
idBaseEnvios = "1BCUxW2yuXlY3iMzvlXO9HPfle78uLiedCUlHBYXBfKA/edit#gid=0"

gc = gs.service_account_from_dict({
  "type": "service_account",
  "project_id": "integracao-389616",
  "private_key_id": os.getenv('KEY_ID'),
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCt+K88L059fRdK\n4qx/ELGiV8rxlUICfvAmAGOsPj38hIPIVENuES+yh9z6fNo0AOPA1xOA1iBUn0F0\nGv8Fh3ttVEeR2bS3ACU/S9UsKqNPjGHz55eBF3qBA4s5zmg/0WXVPXcXoz3ZiJSh\nO1wZSq7lPPp3+OFQJnlrSxDOm+LOXL/7Mf01npkrLAOlE4WSh1/P0W0YvrilDm0Q\nFTKuf4b8TOEE6wRD496ScABWsUyPUUiUjFo7pzbfs8oEXV3Jl0l6XsXzrrcJaV/2\nfNzLEP9nhUbBt3zRd9NOWUMLbmRuupSQ6Kn1odUkNkjVEKQa4iq/pep5dFqD/ufm\nVZ09B5ndAgMBAAECggEAGBe8jOUwRYixVRmXMfGp6AWogVReU+Iod9rN8uibxQDF\nD1U8EV4n8N2H6Nipj1IgOHCQruL4jz+O3PlwH9/nY/isALLZqA5JGj7yQq+U9ktG\ntXR5MtOBj6Rh/5tqLIxfQezFNWzR//I+QyXpV0dUeUK8nSjGa0cowYcfyL0l59YN\n3fVtLSoA0O98/RtPbFwhuqSr6tZWCbhHXzcCVEZ5vRPKZZjSKn8YV4mfrcHTTwfN\nnT0gZf1VaonNH13Q57ptsF/sNSGZjug43/yAo6gbPhLf3q8CpyyHzk1npITHxdfk\n8zQ7Y1YKvCdX8DMd3Oc+60KxHbKT2Sa0khxSm+GrsQKBgQDg8Naw6uW04FwDCHEe\nWT0TqA9BlsV6HHVcnWT3fNmCa0cmJSziUGm1lQ1Gg+kOqzTa6l15PBVn9J4goCEV\nhKdhGqNRzGA2aslYtXxvyu/gHi+thZU/SFKlSYjzRKOlI5HtimrG3V6oIHgx0hwM\nAIMW1HAbCUJdhSX65cqNDH8tewKBgQDF/jEDVXa4buhuX7NP4NkTNpVrRIiB43gz\njQW1hDa3Ll7Dhbr67tDXrncrV8Ku6ufVbzYNs7PJDhUbbLov9+V84q04qj7bURBo\ngNJgIktZjjXz5vuA8YgLE3Ji5wxKVTWpTqqbAwLOoYawsS8XmEC7nnGY0ekPR+LO\nSmsdC756hwKBgQCLVUN3NRlyb+Mu0cTX6qkFiv1gQFc0a3pbEveewYwt1+urei2S\nRgMkwh4GBuGO/4fu7mtWFFyiFwj35ph3rsLLSGfP3EvgiUcNFuXsjYUGi0w3LN6k\n41SmI6WcInFHcoAK5sl7Q1ZFyE8LdT2ARbTtqEuEw7iDG13KSxqrQglpDwKBgE8A\nXEI+Sb7R0kCoQv4uc69s6jYBBI7/WqkHLi39cW+qOvm9VJxnykElRjuvKulspdDO\nLT1OZQBmdBmbSrd1LMamFAQ2Ohp8wBVSwZ7GUFaNng2SLuyGc4gn3E6GbqsCUQUb\ndIuhqe8VGI9MQ8QgZkP2ttEJgPst7dvuacsPMpPlAoGBAJOYzRWwGjULv2hKbzg4\ngF4DE8daKG6VF/Q3J6YTYKoqaNUaNh89MNQMY7/tqse0x+RiQzXVVVGnBeHjCe9D\nv/cZJTFP9AsGW+7yEYz6gTSYMhmNouQ5zd2GbxTwSh5i1KR0P417oVg2qk6M//nt\nCM8PbAq5Bu2ZX2c/ihzvodOj\n-----END PRIVATE KEY-----\n",
  "client_email": "teste-sheets@integracao-389616.iam.gserviceaccount.com",
  "client_id": "115043052029499719431",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/teste-sheets%40integracao-389616.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

def tickets():
    return gc.open_by_url(urlBase + idBaseEnvios).worksheet('tickets').get_values('A2:Z1000')

