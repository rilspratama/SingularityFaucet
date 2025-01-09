import requests,json,time
from logmagix import Logger,LogLevel,Home


home_screen = Home(text="IVY",align="center", adinfo1="The developers are not responsible for any misuse or potential account violations.",adinfo2="Automation Singularity Faucet",credits="Developed by Rils")
log = Logger(prefix="BOT", level=LogLevel.DEBUG,github_repository="https://github.com/rilspratama/SingularityAutoFaucet.git")

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
  'Content-Type': "application/json",
  'accept-language': "en-US,en;q=0.9",
  'cache-control': "max-age=0",
  'origin': "https://faucet-testnet.singularityfinance.ai",
  'priority': "u=1, i",
  'referer': "https://faucet-testnet.singularityfinance.ai/"
}


def get_turnstile_token():
    params = {
        "url":"https://faucet-testnet.singularityfinance.ai",
        "sitekey":"0x4AAAAAAA2Cr3HyNW-0RONo"
    }
    global api_key
    headers = {"X-API-Key":api_key}
    while True:
        response = requests.get(f"https://turnshit.biz.id/turnstile", params=params,headers=headers)
        if response.status_code == 200 and response.json().get("status") == "success":
            log.success("Turnstile token retrieved successfully.")
            return response.json().get("result")
        else:
            log.error("Turnstile token failed to take, try again...")

def startSession(address):
    payload = json.dumps({
      "addr": address,
      "captchaToken": get_turnstile_token()
    })
    log.info(f"Starting sessions for {address}")
    try:
        response = requests.post("https://faucet-testnet.singularityfinance.ai/api/startSession",data=payload,headers=headers)
        data = response.json()
        if response.status_code == 200 and data.get("status") == "claimable":
            log.success("Start sessions success")
            return data.get("session")
        else:
            log.error(f"Failed starting session >>> {response.status_code}")
            return None
    except Exception as e:
        log.error(f"Error on starting session >>> {e}")
        return None



def claimReward(session):
    payload = json.dumps({
      "session": session,
      "captchaToken": get_turnstile_token()
    })
    log.info("Cumming reward session")
    try:
        response = requests.post("https://faucet-testnet.singularityfinance.ai/api/claimReward",data=payload,headers=headers)
        if response.status_code == 200:
            log.success("Claim success!!")
            return True
        else:
            log.error(f"Claim failed >>> {response.status_code}")
            return False
    except Exception as e:
        log.error(f"Claim error >>> {e}")


def getSessionStatus(session):
    params = {
      'session': session,
      'details': "1"
    }
    headers_rx = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
      'accept-language': "en-US,en;q=0.9",
      'priority': "u=1, i",
      'referer': "https://faucet-testnet.singularityfinance.ai/"
    }
    try:
        response = requests.get("https://faucet-testnet.singularityfinance.ai/api/getSessionStatus",headers=headers_rx,params=params)
        data = response.json()
        if response.status_code == 200:
            log.info(f"Tx hash >>> {data.get('claimHash')}")
        else:
            log.error(f"Failed getting status >>> {response.status_code}")
    except Exception as e:
        log.error(f"Error checking status session >>> {e}")



def main():
    home_screen.display()
    global api_key
    api_key = input("Enter api key turnshit(get on @ivy_solver_bot) >>> ")
    with open("address.txt", "r") as file:
        address = file.readlines()
        for a,i in enumerate(address):
            log.info(f"Using address >>> {i}")
            try:
                session = startSession(i)
                if session == None:
                    continue
                claim = claimReward(session)
                if claim:
                    time.sleep(5)
                    getSessionStatus(session)
                else:
                    continue
            except Exception as e:
                log.error(f"Error during process >>> {e}")




















































































































if __name__ == "__main__":
    main()