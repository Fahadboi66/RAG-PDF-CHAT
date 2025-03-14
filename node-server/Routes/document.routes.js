import express from "express";
import { chatWithDocument, getAllDocuments, getDocumentByID, uploadDocument } from "../Controllers/document.controller.js";

const router = express.Router();

router.post("/upload", uploadDocument);
router.post("/chat/:id", chatWithDocument);
router.get("/:id", getDocumentByID);
router.get("/all", getAllDocuments);



export default router;