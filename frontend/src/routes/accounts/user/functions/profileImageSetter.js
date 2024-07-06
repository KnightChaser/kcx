// src/routes/user/functions/profileImageSetter.js

import Cropper from "cropperjs";
import Swal from "sweetalert2";
import { Dropzone } from 'flowbite-svelte';
import { auth } from "../../../../stores/auth";
import "cropperjs/dist/cropper.css";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
const token = auth.getToken();

// Function to set the profile image of the user (upload and crop)
export function profileImageSetter() {
    Swal.fire({
        title: "Select your profile image",
        html: `
            <div id="dropzone" style="border: 2px dashed #ccc; padding: 20px; text-align: center;">
                <svg aria-hidden="true" class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Supported formats: jpg, jpeg, png, gif</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Maximum size: 5,000 x 5,000 pixels</p>
                <input type="file" id="fileInput" accept="image/*" style="display: none;" />
            </div>
        `,
        showCancelButton: true,
        didOpen: () => {
            const dropzone = document.getElementById('dropzone');
            const fileInput = document.getElementById('fileInput');

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

// Handle files from dropzone or input
function handleFiles(files) {
    if (files.length > 0 && validateFile(files[0])) {
        selectedFile = files[0];
    } else {
        Swal.showValidationMessage("Please select a valid image file");
    }
}

// Validate file type and size
function validateFile(file) {
    const validTypes = ["image/jpg", "image/jpeg", "image/png", "image/gif"];
    const maxSize = 5000 * 5000; // 5,000 pixels x 5,000 pixels
    return validTypes.includes(file.type) && file.size <= maxSize;
}

// Using cropper.js to crop the image as the user wants.
function showCropper(imageUrl) {
    Swal.fire({
        title: "Crop your profile image",
        html: `
            <img id="cropperImage" src="${imageUrl}" style="max-width: 100%; display: block; margin-bottom: 1rem;">
            <input type="range" id="zoomRange" min="0.1" max="3" step="0.1" value="1" style="width: 100%;">
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
