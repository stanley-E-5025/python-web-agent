from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Note, NoteBase
from ..database import get_session
from ..crud import get_notes, create_note, get_note, update_note, delete_note

router = APIRouter()

@router.get("/notes")
def read_notes(session = Depends(get_session)):
    return get_notes(session)

@router.post("/notes", response_model=Note)
def create_note_endpoint(note: NoteBase, session = Depends(get_session)):
    return create_note(session, note)

@router.get("/notes/{note_id}", response_model=Note)
def read_note_endpoint(note_id: int, session = Depends(get_session)):
    note = get_note(session, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=Note)
def update_note_endpoint(note_id: int, note: NoteBase, session = Depends(get_session)):
    updated_note = update_note(session, note, note_id)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@router.delete("/notes/{note_id}", response_model=Note)
def delete_note_endpoint(note_id: int, session = Depends(get_session)):
    deleted_note = delete_note(session, note_id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted_note
