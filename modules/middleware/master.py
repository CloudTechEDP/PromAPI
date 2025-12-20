from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from a2wsgi import ASGIMiddleware
import os
import inspect
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
import re
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from modules.middleware.print_response import *

from modules.model.model import *
from modules.repository.db import *

from modules.api.gauge import router as gauge_router
from modules.api.counter import router as counter_router
from modules.api.aggregate import router as aggregate_router

from modules.routes.index import router as index_router