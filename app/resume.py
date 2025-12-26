import os
import glob
import uuid
from PyPDF2 import PdfReader
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings


class Resume:
    def __init__(self, dataset_folder=None):
        # Default dataset folder relative to this script
        if dataset_folder is None:
            dataset_folder = os.path.join(os.path.dirname(__file__), "../dataset")

        # Find all PDFs
        pdf_files = glob.glob(os.path.join(dataset_folder, "*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {dataset_folder}")
        self.file_path = pdf_files[0]  # Take the first PDF
        print(f"Using PDF: {self.file_path}")

        # Initialize ChromaDB client with persistence
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="vectorstore"  # Directory for storing vectors
        ))
        self.collection = self.chroma_client.get_or_create_collection(name="resume")

        #HuggingFace embedding model (local, free)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load PDF chunks
        self.chunks = self._load_pdf_chunks()

    def _load_pdf_chunks(self, chunk_size=1000):
        """Read PDF and split into text chunks."""
        pdf = PdfReader(self.file_path)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # Split into chunks
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        print(f"Total chunks created: {len(chunks)}")
        return chunks

    def load_resume(self):
        """Load resume chunks into ChromaDB with embeddings."""
        if self.collection.count() == 0:
            for chunk in self.chunks:
                vector = self.embeddings.embed_query(chunk)
                self.collection.add(
                    documents=[chunk],
                    metadatas=[{"source": self.file_path}],
                    ids=[str(uuid.uuid4())],
                    embeddings=[vector]  #store semantic vector
                )
            print("Resume loaded into ChromaDB with embeddings.")
        else:
            print("Resume already loaded in ChromaDB.")

    def query_resume(self, query_text, n_results=2):
        """Query resume for most relevant chunks to a text query."""
        query_vector = self.embeddings.embed_query(query_text)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=n_results
        )
        return results.get("documents", [])

    def match_with_job(self, skills: list, n_results=3):
        """Match resume against job skills and return relevant chunks."""
        if not skills:
            return []
        query_text = " ".join(skills)
        return self.query_resume(query_text, n_results=n_results)


if __name__ == "__main__":
    # For manual testing
    resume = Resume()
    resume.load_resume()

    while True:
        query = input("\nEnter a query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = resume.query_resume(query)
        if results and results[0]:
            print("\nResults:")
            for i, res in enumerate(results[0], 1):
                print(f"{i}: {res}\n")
        else:
            print("No results found.")




