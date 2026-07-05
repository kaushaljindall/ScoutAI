from sqlalchemy.orm import Session
from app.models.documents import Document, DocumentTemplate, Branding
from app.schemas.documents import DocumentCreate, DocumentUpdate, DocumentTemplateCreate, BrandingBase
from datetime import datetime

class DocumentService:
    @staticmethod
    def get_documents(db: Session, user_id: str):
        return db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()

    @staticmethod
    def get_document(db: Session, doc_id: str, user_id: str):
        return db.query(Document).filter(Document.id == doc_id, Document.user_id == user_id).first()

    @staticmethod
    def create_document(db: Session, user_id: str, doc_in: DocumentCreate):
        doc = Document(
            user_id=user_id,
            lead_id=doc_in.lead_id,
            title=doc_in.title,
            type=doc_in.type,
            content=doc_in.content,
            status=doc_in.status,
            version=doc_in.version
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def update_document(db: Session, doc_id: str, user_id: str, doc_in: DocumentUpdate):
        doc = db.query(Document).filter(Document.id == doc_id, Document.user_id == user_id).first()
        if not doc:
            raise ValueError("Document not found")
            
        for key, value in doc_in.model_dump(exclude_unset=True).items():
            setattr(doc, key, value)
            
        doc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def delete_document(db: Session, doc_id: str, user_id: str):
        doc = db.query(Document).filter(Document.id == doc_id, Document.user_id == user_id).first()
        if not doc:
            raise ValueError("Document not found")
        db.delete(doc)
        db.commit()
        return True

class TemplateService:
    @staticmethod
    def get_templates(db: Session, user_id: str):
        return db.query(DocumentTemplate).filter(DocumentTemplate.user_id == user_id).all()

    @staticmethod
    def create_template(db: Session, user_id: str, template_in: DocumentTemplateCreate):
        template = DocumentTemplate(
            user_id=user_id,
            name=template_in.name,
            category=template_in.category,
            content=template_in.content
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

class BrandingService:
    @staticmethod
    def get_branding(db: Session, user_id: str):
        brand = db.query(Branding).filter(Branding.user_id == user_id).first()
        if not brand:
            brand = Branding(user_id=user_id)
            db.add(brand)
            db.commit()
            db.refresh(brand)
        return brand

    @staticmethod
    def update_branding(db: Session, user_id: str, brand_in: BrandingBase):
        brand = BrandingService.get_branding(db, user_id)
        for key, value in brand_in.model_dump(exclude_unset=True).items():
            setattr(brand, key, value)
        db.commit()
        db.refresh(brand)
        return brand
