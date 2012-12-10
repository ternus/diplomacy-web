# -*- coding: utf-8 -*-
"""Models for Diplomacy."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref
from constants import *

from diplomacy.model import DeclarativeBase, metadata, DBSession

def get_turn():
    return 1

class Faction(DeclarativeBase):
    """
    A Diplomacy faction.
    """
    __tablename__ = 'faction'
    name = Column(Unicode, primary_key=True)
    units = relation("Unit")
    provinces = relation("Province")

class Province(DeclarativeBase):
    """
    A Diplomacy province.
    """
    __tablename__ = 'province'
    name = Column(Unicode, primary_key=True)
#    province_type = Column(Integer)
    province_special = Column(Unicode)
    faction_name = Column(Unicode, ForeignKey('faction.name'))
    unit = relation("Unit")

    def neighbors(self):
        return DBSession.query(Province)

class ProvinceAdj(DeclarativeBase):
    """
    A bidirectional many-to-many link between two Provinces.
    Cargo-culted from https://groups.google.com/forum/?fromgroups=#!topic/sqlalchemy/325FGFXROmA 
    """
    __tablename__ = 'provinceadj'
    province_name = Column(Unicode, ForeignKey('province.name'), primary_key=True)
    adj_province_name = Column(Unicode, ForeignKey('province.name'), primary_key=True)
    province = relation("Province",  primaryjoin=province_name==Province.name, backref="adj_province")
    adj_province = relation("Province",  primaryjoin=adj_province_name==Province.name, backref="province")

class Unit(DeclarativeBase):
    """
    A single unit.
    Why have a special model just for units?  To support "special" units in variant versions.
    """
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True)
    faction_id = Column(Unicode, ForeignKey('faction.name'))
    province_name = Column(Unicode, ForeignKey('province.name'))
    unit_type = Column(Unicode)
 
class SupportOrder(DeclarativeBase):
    """ 
    Used for Supports and Convoys.
    """
    __tablename__ = 'supportorder'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    support_source = Column(Unicode, ForeignKey('province.name')) 
    support_target = Column(Unicode, ForeignKey('province.name')) 
    support_order_type = Column(Unicode) # Support or Convoy
    support_unit_type = Column(Unicode)

class Order(DeclarativeBase):
    """
    A single Diplomacy order.
    """
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    turn = Column(Integer)
    faction_name = Column(Unicode, ForeignKey('faction.name'))
    order_type = Column(Unicode)
    unit_id = Column(Integer, ForeignKey('unit.id'))
    target = Column(Unicode, ForeignKey('province.name'))
    support_order = relation("SupportOrder", backref=backref("order", uselist=False))

    def is_committed(self):
        """ 
        Can this order be undone?
        """
        return not (self.turn == get_turn())

    def valid_support_order(self):
        pass
