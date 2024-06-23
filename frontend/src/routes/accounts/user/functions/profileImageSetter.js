// src/routes/user/functions/profileImageSetter.js

import Cropper from "cropperjs";
import Swal from "sweetalert2";
import { auth } from "../../../../stores/auth";
import "cropperjs/dist/cropper.css";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
const token = auth.getToken();

// Function to set the profile image of the user. (upload and crop)
export function profileImageSetter() {
    // First, get uploaded image file from the user's PC on the modal.
    Swal.fire({
        title: "Select your profile image",
        input: "file",
        inputAttributes: {
            accept: "image/*",
            "aria-label": "Upload your profile image"
        },
        showCancelButton: true,
        preConfirm: (file) => {
            if (!file) {
                Swal.showValidationMessage("Please select an image");
                return false;
            }
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    resolve(e.target.result);
                };
                reader.readAsDataURL(file);
            });
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const imageUrl = result.value;
            showCropper(imageUrl);
        }
    });
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
            // @ts-ignore
            const cropper = new Cropper(image, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                ready: function() {
                    zoomRange.addEventListener("input", function() {
                        // @ts-ignore
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
        })
    } catch (error) {
        Swal.fire({
            icon: "error",
            title: "Failed to upload image",
            text: error.message,
        });
    }
}
