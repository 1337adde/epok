from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# Create an instance of FastAPI
app = FastAPI()

# Creates the tables in the database
models.Base.metadata.create_all(bind=engine)

# Start a database session
def get_db():
     try:
          db = SessionLocal()
          yield db
     finally:
          db.close()

class Modul(BaseModel):
     kurskod: str
     modulnamn: str
     poang: float

class UppdateraModul(BaseModel):
     kurskod: Optional[str] = None
     modulnamn: Optional[str] = None
     poang: Optional[float] = None

# - - - - - - - - - - - - - - - - - - - - - - - - - 

# GET functions 
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Moduler).all()

@app.get("/{kurskod}")
def get_modul(kurskod : str, db: Session = Depends(get_db)):
    moduler = db.query(models.Moduler).filter(models.Moduler.kurskod == kurskod.upper()).all()
    if not moduler:
        raise HTTPException(status_code=404, detail="Kurskoden kunde inte hittas")
    return moduler

# - - - - - - - - - - - - - - - - - - - - - - - - - 

# POST skapa ny modul
@app.post("/skapa-modul/")
def skapa_modul(modul : Modul, db: Session = Depends(get_db)):
     
     modul_modell = models.Moduler()
     modul_modell.kurskod = modul.kurskod
     modul_modell.modulnamn = modul.modulnamn
     modul_modell.poang = modul.poang

     db.add(modul_modell)
     db.commit()

     return modul_modell

# - - - - - - - - - - - - - - - - - - - - - - - - - 

# PUT uppdatera modul
@app.put("/uppdatera-modul/{modul_id}")
def uppdatera_modul(modul_id : int, modul : UppdateraModul, db: Session = Depends(get_db)):
     
     # Hitta modulen i databasen
     modul_modell = db.query(models.Moduler).filter(models.Moduler.id == modul_id).first()
     if modul_modell is None:
          raise HTTPException(status_code=404, detail="Modulen kunde inte hittas")
     
     # If-satserna ser till att värden inte skrivs över med null
     if modul.modulnamn != None:
          modul_modell.modulnamn = modul.modulnamn
     if modul.kurskod != None:
          modul_modell.kurskod = modul.kurskod
     if modul.poang != None:
          modul_modell.poang = modul.poang

     db.add(modul_modell)
     db.commit()

     return modul_modell

# - - - - - - - - - - - - - - - - - - - - - - - - - 

# DELETE radera modul
@app.delete("/radera-modul/{modul_id}")
def radera_modul(modul_id : int, db: Session = Depends(get_db)):
     modul_modell = db.query(models.Moduler).filter(models.Moduler.id == modul_id).first()
     if modul_modell is None:
          raise HTTPException(status_code=404, detail="Modulen kunde inte hittas")

     db.delete(modul_modell)
     db.commit()

     return {"Message" : "Modul raderad"}
