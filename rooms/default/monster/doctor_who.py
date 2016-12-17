from localizations import locale_manager
from constants import *
import time
import databasemanager

name = locale_manager.get('rooms.default.monster.doctor_who.phrase_1')

hp = 25 * 1.01 ** (databasemanager.get_variable('doctor_num', 1) - 1)
damage_range =  ( 0, 50 )

coins = 0

loot = [ 'fez', 'laser_screwdriver' ]

def can_open(user, reply):
	return not user.has_tag(DEVIL)

def open_failure(user, reply):
	reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_2'))

def enter(user, reply):
	reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_3'))

	number = databasemanager.get_variable('doctor_num', 1)
	name = databasemanager.get_variable('doctor_killer')

	user.set_room_temp('hp_max', hp)

	reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_7').format(number), photo=DOCTOR_WHO_STICKER)

	if name is not None:
		t = time.time() - databasemanager.get_variable('doctor_kill_time', time.time()+1000)

		reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_8').format(name))

		if t > 0:
			reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_9').format(t / 60))

def get_actions(user):
	return user.get_fight_actions() + [ locale_manager.get('rooms.default.monster.doctor_who.phrase_4')]

def make_damage(user, reply, dmg):
	hp = user.get_room_temp('hp', 0)
	hp -= max(1, dmg)

	if hp <= 0:
		number = databasemanager.get_variable('doctor_num', 1)
		databasemanager.set_variable('doctor_num', number + 1)
		databasemanager.set_variable('doctor_killer', user.name)
		databasemanager.set_variable('doctor_kill_time', time.time())

		databasemanager.add_to_leaderboard(user, user.get_room_temp('hp_max', 10 ** 5), databasemanager.DOCTOR_TABLE)
		user.won(reply)
	else:
		user.set_room_temp('hp', hp)

def action(user, reply, text):
	if text == locale_manager.get('rooms.default.monster.doctor_who.phrase_5'):
		reply(locale_manager.get('rooms.default.monster.doctor_who.phrase_6'))

		user.leave(reply)
	else:
		user.fight_action(reply, text)
