import mongoose, { Schema } from "mongoose";

const documentSchema = new Schema({
    username: {
        type: String,
        trim: true,
        required: true,
    },

    docID : {  // Bucket File ID
        type: String,
        required: true
    },

    docName: {
        type: String,
        trim: true,
    },

    docType: {
        type: String,
        enum: ["doc", "docx", "pdf", "ppt", "pptx", "xls", "xlsx"],
        required: true,
    },

    docSize : {
        type:  String,
        required: true,
    }

}, {timestamps: true});


export const Document = mongoose.model("Document", documentSchema);