import { Document } from "../Models/document.modal.js";
import axios from "axios";

export const uploadDocument = async (req, res) => {
    const { username, docID, docName, docType, docSize } = req.body;

    // Validate input
    if (!username || !docID || !docType || !docSize) {
        return res.status(400).send({
            success: false,
            data: {},
            message: "Please provide all information to upload a file",
        });
    }

    try {
        // Save document metadata in MongoDB
        const newDocument = new Document({
            username,
            docID,
            docName,
            docType,
            docSize,
        });
        await newDocument.save();

        // Send the file to the Python server for processing
        const pythonServerResponse = await axios.post(
            "http://localhost:8001/saveDoc",
            {
                file_path: `/documents/${docName}`,  // Path to the uploaded file
                metadata: {
                    mongo_id: docID,  // Use docID as the MongoDB ID
                    author: username,
                    title: docName,
                },
            }
        );

        // Return success response
        res.status(200).send({
            success: true,
            data: pythonServerResponse.data,
            message: "Document uploaded and processed successfully",
        });
    } catch (error) {
        console.error("Error uploading document:", error);
        res.status(500).send({
            success: false,
            data: {},
            message: "Failed to upload document",
        });
    }
};


export const chatWithDocument = async (req, res) => {
    const { docID, query } = req.body;

    // Validate input
    if (!docID || !query) {
        return res.status(400).send({
            success: false,
            data: {},
            message: "Please provide docID and query",
        });
    }

    try {
        // Send the query to the Python server
        const pythonServerResponse = await axios.post(
            "http://localhost:8001/queryDoc",
            {
                mongo_id: docID,  // Use docID as the MongoDB ID
                query: query,
            }
        );

        // Return the results
        res.status(200).send({
            success: true,
            data: pythonServerResponse.data,
            message: "Query processed successfully",
        });
    } catch (error) {
        console.error("Error querying document:", error);
        res.status(500).send({
            success: false,
            data: {},
            message: "Failed to query document",
        });
    }
};



export const getDocumentByID = async (req, res) => {
   const {id} = req.params;

   try {
        const doc = await Document.find({ _id: id});
        if(!doc) {
            res.status(404).send({success: false, data: {}, message: "Document not found"})
        }

        res.status(200).send({success: true, data: doc, message: "Document Details Fetched Successfully"})
   
    } catch (err) {
        res.status(500).send({success: false, data: {}, message: "Server error - Please try again later"})
    }

}


export const getAllDocuments = async (req, res) => {
    const username = req.body.username;

    try {
        const docs = await Document.find({username});

        if(!docs) {
            res.status(404).send({success: false, data: {}, message: "No Document found for this user"})
        }

        res.status(200).send({success: true, data: docs, message: "Document Fetched Successfully"});
        
    } catch (err) {
        res.status(500).send({success: false, data: {}, message: "Server Error - Please try again later"});
        
    } 
}