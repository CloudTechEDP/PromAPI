from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from a2wsgi import ASGIMiddleware
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import sys
import shutil
import uvicorn
import webbrowser
import asyncio
import os
import inspect
import re
import json
import inspect

load_dotenv()

from modules.middleware.util import *
from modules.model.model import *
from modules.repository.db import *
from modules.middleware.openrouter_free import *
from modules.api.gauge import router as gauge_router
from modules.api.counter import router as counter_router
from modules.api.aggregate import router as aggregate_router
from modules.routes.index import router as index_router