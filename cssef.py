#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.exc import NoSuchTableError
from datetime import datetime
import ConfigParser
import sys
from time import sleep
from random import randrange

class Database:
    def __init__(self, conf):
        database_address = "%s://%s:%s@%s:%s/%s" % (conf["type"], \
            conf["user"], conf["password"], conf["address"], conf["port"], \
            conf["db"])
        self.db = create_engine(database_address)
        self.md = MetaData(self.db)
        try:
            self.tb = self.tables_load(self.md)
        except NoSuchTableError:
            self.sync()

    def sync(self):
        tables = self.tables_define(self.md)
        self.tables_create(tables)

    def tables_define(self, md):
        scores = Table('scores', md,
            Column('datetime', DateTime),
            Column('team', String(10)),
            Column('addr', String(15)),
            Column('port', Integer),
            Column('status', Boolean))
        tables = {}
        tables["scores"] = scores
        return tables

    def tables_load(self):
        tables = {}
        tables["scores"] = Table('scores', md, autoload=True)
        return tables

    def tables_create(self, tables_dict):
        for i in tables_dict:
            tables_dict[i].create()

    def new_score(self, team, addr, port, status):
        insert = self.tb["scores"].insert()
        fields = {
            'datetime': datetime.now(),
            'team': team,
            'addr': addr,
            'port': port,
            'status': status
        }
        insert.execute(fields)

class Configuration:
    def __init__(self):
        self.general_config_path = "cssef.conf"
        self.teams_config_path = "teams.conf"
        self.pluggins_config_path = "pluggins.conf"

        self.general = self.file_map(self.general_config_path)
        self.teams = self.file_map(self.teams_config_path)
        self.pluggins = self.file_map(self.pluggins_config_path)

    def file_map(self, config_path):
        dict1 = {}
        config_obj = self.load_file(config_path)
        for i in config_obj.sections():
            dict1[i] = self.section_map(config_obj, i)
        return dict1

    def load_file(self, config_path):
        conf = ConfigParser.ConfigParser()
        conf.readfp(open(config_path))
        return conf

    def section_map(self, config_obj, section):
        dict1 = {}
        options = config_obj.options(section)
        for option in options:
            try:
                dict1[option] = config_obj.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

class Team:
    list = []
    def __init__(self, team_conf):
        self.id = team_conf["id"]
        self.name = team_conf["name"]
        self.net_addr = team_conf["net_addr"]

def log(team, service, status):
    if status:
        print "Service '%s' for team '%s' was marked 'up'." % (service,team)
    else:
        print "Service '%s' for team '%s' was marked 'down'." % (service,team)

def pluggin_module(pluggin_obj):
    module_string = pluggin_obj["module"]
    module = __import__('pluggins.' + module_string, fromlist=[module_string])
    return getattr(module, module_string)(pluggin_obj)

def team_factory(conf):
    teams_list = []
    for i in conf.teams:
        teams_list.append(Team(conf.teams[i]))
    return teams_list

def service_factory(conf):
    service_list = []
    for i in conf.pluggins:
        service_list.append(pluggin_module(conf.pluggins[i]))
    return service_list

def run_loop(teams, services):
    condition = True
    while(condition):
        #sleep(rand_time_range())
        for i in services:
            for t in teams:
                result = i.score(t)
                log(t.name, i.name, result)
        break

def rand_time_range():
    sleep_time = randrange(180,300)
    sleep(sleep_time)

def main():
    conf = Configuration()
    #db = Database(conf.general)
    teams = team_factory(conf)
    services = service_factory(conf)

    run_loop(teams, services)

main()