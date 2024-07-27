FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

COPY ./peer.py peer.py
