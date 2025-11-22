import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    original_note = Column(Text, nullable=False)
    soap_note = Column(JSON)
    key_vitals = Column(JSON)
    exam_findings = Column(JSON)
    key_information = Column(JSON)
    specialty = Column(String, default="General")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    if engine is None:
        raise ValueError("Database not configured. DATABASE_URL environment variable is required.")
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@st.cache_resource
def get_cached_engine():
    return engine

def save_clinical_note(original_note: str, result: dict, specialty: str = "General"):
    if SessionLocal is None:
        raise ValueError("Database not configured")
    db = SessionLocal()
    try:
        note = ClinicalNote(
            original_note=original_note,
            soap_note=result.get("soap_note", {}),
            key_vitals=result.get("key_vitals", {}),
            exam_findings=result.get("exam_findings", []),
            key_information=result.get("key_information", {}),
            specialty=specialty
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note.id
    finally:
        db.close()

def get_all_notes(limit: int = 100):
    if SessionLocal is None:
        return []
    db = SessionLocal()
    try:
        notes = db.query(ClinicalNote).order_by(ClinicalNote.created_at.desc()).limit(limit).all()
        return notes
    finally:
        db.close()

def search_notes(query: str):
    if SessionLocal is None:
        return []
    db = SessionLocal()
    try:
        notes = db.query(ClinicalNote).filter(
            ClinicalNote.original_note.ilike(f"%{query}%")
        ).order_by(ClinicalNote.created_at.desc()).all()
        return notes
    finally:
        db.close()

def filter_notes_by_specialty(specialty: str):
    if SessionLocal is None:
        return []
    db = SessionLocal()
    try:
        notes = db.query(ClinicalNote).filter(
            ClinicalNote.specialty == specialty
        ).order_by(ClinicalNote.created_at.desc()).all()
        return notes
    finally:
        db.close()

def get_note_by_id(note_id: int):
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        note = db.query(ClinicalNote).filter(ClinicalNote.id == note_id).first()
        return note
    finally:
        db.close()

def delete_note(note_id: int):
    if SessionLocal is None:
        return False
    db = SessionLocal()
    try:
        note = db.query(ClinicalNote).filter(ClinicalNote.id == note_id).first()
        if note:
            db.delete(note)
            db.commit()
            return True
        return False
    finally:
        db.close()
