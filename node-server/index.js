import express from "express"
import cors from "cors"
import dotenv from "dotenv"
import connectDB from "./Database/connection.js";
dotenv.config();

const PORT = process.env.PORT || 5000;


const app = express();
app.use(express.json());
app.use(cors({
    origin: "*",
}));

import docRouter from "./Routes/document.routes.js"

app.use("/api/v1/document", docRouter);

connectDB()
    .then(() => {
        app.listen(PORT, () => {
            console.log(`Server is listening on port ${PORT}`);
        });
    })
    .catch((err) => {
        console.error("Server failed to start due to DB connection error:", err.message);
    });





