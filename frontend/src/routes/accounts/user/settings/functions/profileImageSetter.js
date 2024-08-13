// src/routes/user/settings/functions/profileImageSetter.js

import Cropper from "cropperjs";
import Swal from "sweetalert2";
import { auth } from "../../../../../stores/auth";
import "cropperjs/dist/cropper.css";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
const token = auth.getToken();

// Function to set the profile image of the user (upload and crop)
export function profileImageSetter() {
    Swal.fire({
        title: "Select your profile image",
        html: `
            <div id="dropzone" style="border: 2px dashed #ccc; padding: 20px; text-align: center;">
                <svg aria-hidden="true" 
                     class="mb-3 w-10 h-10 text-gray-400"
                     style="position: relative; left: 50%; transform: translateX(-50%);"
                     fill="none" stroke="currentColor" viewBox="0 0 24 24" 
                     xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p id="dropzoneText" class="mb-2 text-sm text-gray-500 dark:text-gray-400">
                    <span class="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Supported formats: JPEG, PNG, GIF, SVG</p>
                <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">Maximum size: 5,000 x 5,000 pixels</p>
                <input type="file" id="fileInput" accept="image/*" style="display: none;" />
            </div>
        `,
        showCancelButton: true,
        didOpen: () => {
            const dropzone = document.getElementById('dropzone');
            const fileInput = document.getElementById('fileInput');
            const dropzoneText = document.getElementById('dropzoneText');

            dropzone.addEventListener('click', () => fileInput.click());
            dropzone.addEventListener('dragover', (event) => {
                event.preventDefault();
            });
            dropzone.addEventListener('drop', (event) => {
                event.preventDefault();
                handleFiles(event.dataTransfer.files);
            });
            fileInput.addEventListener('change', (event) => {
                handleFiles(event.target.files);
            });

            function handleFiles(files) {
                if (files.length > 0 && validateFile(files[0])) {
                    selectedFile = files[0];
                    dropzoneText.innerHTML = `<strong>File Name: <code>${selectedFile.name}</code>, Size: ${(selectedFile.size / 1024).toFixed(2)} KiB</strong>`;
                } else {
                    Swal.showValidationMessage("Please select a valid image file");
                }
            }
        }
    }).then((result) => {
        if (result.isConfirmed && selectedFile) {
            const reader = new FileReader();
            reader.onload = (e) => {
                showCropper(e.target.result);
            };
            reader.readAsDataURL(selectedFile);
        }
    });
}

let selectedFile = null;

// Validate file type and size
function validateFile(file) {
    const validTypes = ["image/jpeg", "image/png", "image/gif", "image/svg+xml"];
    const maxSize = 5000 * 5000; // Example size limit in bytes
    return validTypes.includes(file.type) && file.size <= maxSize;
}

// Using cropper.js to crop the image as the user wants.
function showCropper(imageUrl) {
    Swal.fire({
        title: "Crop your profile image",
        html: `
            <div style="width: 100%; height: 400px; overflow: hidden;">
                <img id="cropperImage" src="${imageUrl}" style="max-width: 100%; display: block; margin-bottom: 1rem;">
                <input type="range" id="zoomRange" min="0.1" max="3" step="0.1" value="1" style="width: 100%;">
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: "Upload",
        willOpen: () => {
            const image = document.getElementById("cropperImage");
            const zoomRange = document.getElementById("zoomRange");
            const cropper = new Cropper(image, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                responsive: true,
                ready: function() {
                    zoomRange.addEventListener("input", function() {
                        cropper.zoomTo(parseFloat(this.value));
                    });
                }
            });

            Swal.getConfirmButton().addEventListener("click", () => {
                cropper.getCroppedCanvas({
                    width: 256,
                    height: 256,
                }).toBlob((blob) => {
                    uploadCroppedImage(blob);
                });
            });
        }
    });
}

// Function to upload the cropped image to the server.
async function uploadCroppedImage(blob) {
    const formData = new FormData();
    formData.append("file", blob, "profile.png");

    try {
        const response = await fetch(`${BACKEND_API_URL}/account/upload-profile-image`, {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}` 
            }
        });
        if (!response.ok) {
            throw new Error("Failed to upload image");
        }
        Swal.fire({
            icon: "success",
            title: "Image uploaded successfully",
            text: "The change will be applied immediately."
        }).then(() => {
            // Reload the page to see the changes
            location.reload();
        });
    } catch (error) {
        Swal.fire({
            icon: "error",
            title: "Failed to upload image",
            text: error.message,
        });
    }
}
