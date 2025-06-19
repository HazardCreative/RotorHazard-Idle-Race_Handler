''' Idle race handler '''

# stops a race when no passes have arrived in [x] seconds

import gevent
from time import monotonic
from eventmanager import Evt
from RHUI import UIField, UIFieldType, UIFieldSelectOption

class AutoRestart:
	def __init__(self, rhapi):
		self._rhapi = rhapi
		self.thread_fn = None
		self.active = False
		self.activity_timestamp = 0

	def on_race_stop(self, _evtargs):
		self.active = False

	def on_race_lap(self, _evtargs):
		self.active = True
		self.update_expire_thread(monotonic())

	def update_expire_thread(self, time_now):
		self.activity_timestamp = time_now
		if self.thread_fn:
			self.thread_fn.kill(block=False)
		self.thread_fn = gevent.spawn(self.check_time_expired)

	def check_time_expired(self):
		expire_time = 1
		while expire_time > 0:
			expire_time = self.activity_timestamp + self._rhapi.db.option('idle_race_sec', as_int=True) - monotonic()
			if expire_time > 0:
				gevent.sleep(1)

		if self.active and self._rhapi.db.option('idle_race_sec', as_int=True) > 0:
			self._rhapi.race.stop()
			
			if self._rhapi.db.option('idle_behavior') in ['save', 'restart']:
				self._rhapi.race.save()
				
				if self._rhapi.db.option('idle_behavior') == 'restart':
					self._rhapi.race.stage()

def initialize(rhapi):
	autorestart = AutoRestart(rhapi)

	rhapi.events.on(Evt.RACE_STOP, autorestart.on_race_stop)
	rhapi.events.on(Evt.RACE_LAP_RECORDED, autorestart.on_race_lap)
	
	rhapi.ui.register_panel('idle_race_handler', 'Idle Race Handler', 'run', order=0)
	rhapi.fields.register_option(
		UIField('idle_race_sec', "Idle After (Seconds)", UIFieldType.BASIC_INT, value = 60, desc="0 to disable"),
		'idle_race_handler'
	)
	rhapi.fields.register_option(
		UIField('idle_behavior', "Idle Action", UIFieldType.SELECT, options=[
                UIFieldSelectOption('stop', "Stop"),
                UIFieldSelectOption('save', "Stop, Save"),
                UIFieldSelectOption('restart', "Stop, Save, Restart"),
            ], value='stop'),
		'idle_race_handler'
	)


