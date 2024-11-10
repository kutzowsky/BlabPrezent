#!/usr/bin/env python

import argparse
import logging
import os.path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from dal import datamanager
from workers import XmppBot, WebsiteParsingBot, gift_assignment_draw, GiftAssignmentSender

logger = logging.getLogger()


def exit_if_config_not_exist():
    conf_file = 'configuration.toml'
    if not os.path.exists('configuration.toml'):
        logger.error(f'{conf_file} does not exist. Provide valid configuration file and try again.')
        sys.exit(1)


def set_logger():
    logger.setLevel(settings.General.log_level.upper())
    file_handler = logging.FileHandler(settings.General.log_file)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def create_db_if_not_exist():
    if not os.path.exists(settings.General.database_file):
        logger.warning(f'Database file does not exist. Creating.')
        datamanager.create_db()


def action_bot():
    if settings.General.mode == 'www':
        logger.info('Starting WWW bot')

        bot = WebsiteParsingBot()
        bot.login(settings.WebsiteBot.login, settings.WebsiteBot.password)
        bot.try_create_latest_message_file()
        bot.start_listening()

    elif settings.General.mode == 'xmpp':
        logger.info('Starting XMPP bot')

        bot = XmppBot(settings.JabberBot.jid, settings.JabberBot.password, settings.JabberBot.blabler_bot_jid)
        bot.connect()
        bot.process()


def action_draw():
    gift_assignment_draw()


def action_send_assignments():
    sender = GiftAssignmentSender(mode=settings.General.mode)
    sender.send_assignments()


def action_status_users():
    user_data = datamanager.get_all_addresses()
    print(f'Uczestników: {len(user_data)}')
    for user_entry in user_data:
        print(f'{user_entry[0]: <13}{user_entry[1]}')


def action_status_gifts():
    packages = datamanager.get_all_not_sent_packages()
    print(f'Niewysłane: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]}')
    print()

    packages = datamanager.get_all_sent_packages()
    print(f'W drodze: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]: <13}{package[2]} {package[3] or ""}')
    print()

    packages = datamanager.get_all_received_packages()
    print(f'Odebrane: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]: <13}{package[2]} {package[3]} {package[4] or ""}')


def create_parser():
    parser = argparse.ArgumentParser(description='Blabprezent CLI')
    subparsers = parser.add_subparsers(dest='mode', help='Available modes')
    subparsers.add_parser('bot', help='Start bot')
    subparsers.add_parser('draw', help='Gift draw')
    subparsers.add_parser('send-assignments', help='Send gift assignments')
    status_parser = subparsers.add_parser('status', help='Check status')
    status_subparsers = status_parser.add_subparsers(dest='status_type', help='Status type')
    status_subparsers.add_parser('users', help='Check participant list')
    status_subparsers.add_parser('gifts', help='Check gift status')
    return parser, status_parser


def run_action_from_arguments():
    parser, status_parser = create_parser()

    args = parser.parse_args()

    logger.debug(f'Selected mode: {args.mode}')

    if args.mode == 'bot':
        action_bot()
    elif args.mode == 'draw':
        action_draw()
    elif args.mode == 'send-assignments':
        action_send_assignments()
    elif args.mode == 'status':
        if args.status_type == 'users':
            action_status_users()
        elif args.status_type == 'gifts':
            action_status_gifts()
        else:
            status_parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    exit_if_config_not_exist()
    set_logger()
    create_db_if_not_exist()
    run_action_from_arguments()
