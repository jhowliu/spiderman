#!/usr/bin/env python
# -*- coding=utf-8 -*-
from sqlalchemy import func
from schema import HouseInfo1, meta
from engine import sess

# QUERY STATEMENT
result = sess.query(HouseInfo1.CaseFrom, func.count(HouseInfo1.CaseFrom)) \
             .group_by(HouseInfo1.CaseFrom).all()
print(result)

# INSERT STATEMENT add_all(list of class) or add
