# @app.put("/ratings/{rating_uuid}", response_model=schemas.Rating)
# def update_rating(rating_uuid: uuid.UUID, rating: schemas.RatingUpdate, db: Session = Depends(get_db)):
#     db_rating = db.query(models.Rating).filter(models.Rating.rating_uuid == rating_uuid).first()
#     if db_rating is None:
#         raise HTTPException(status_code=404, detail="Rating not found")
#     for key, value in rating.dict(exclude_unset=True).items():
#         setattr(db_rating, key, value)
#     db.commit()
#     db.refresh(db_rating)
#     return db_rating