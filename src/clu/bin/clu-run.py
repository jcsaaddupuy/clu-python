from clu.probes.mpdprobestatus import MpdProbeStatus
import logging

logging.basicConfig(level=logging.INFO)

agentconf={"channel":{"exchange":"home.events","type":"topic"},"messages":{"routing_key":"home.events.multimedia.music.mpd.state"}}
mpdconf={"host":"mpd.lan", "password":"password"}
rmqconf={"host":"192.168.0.5", "user":"guest", "passwword":"guest"}
agent=MpdProbeStatus(agentconf, mpdconf, rmqconf)

#Call
while True:
  agent.run()
