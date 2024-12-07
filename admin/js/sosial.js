let mediaItems = [
    { id: 1, type: 'photo', url: 'https://exaple.com/photo1.jpg' },
    { id: 2, type: 'video', url: 'https://example.com/video1.mp4', thumbnailUrl: 'https://exaple.com/photo1.jpg' },
    { id: 3, type: 'photo', url: 'https://exaple.com/photo1.jpg' },
    { id: 4, type: 'video', url: 'https://example.com/video2.mp4', thumbnailUrl: 'https://exaple.com/photo1.jpg' },
];

const mediaTableBody = document.getElementById('mediaTableBody');
const mediaForm = document.getElementById('mediaForm');
const mediaType = document.getElementById('mediaType');
const photoInputs = document.getElementById('photoInputs');
const videoInputs = document.getElementById('videoInputs');
const photoUpload = document.getElementById('photoUpload');
const thumbnailUpload = document.getElementById('thumbnailUpload');
const videoUpload = document.getElementById('videoUpload');
const photoPreview = document.getElementById('photoPreview');
const thumbnailPreview = document.getElementById('thumbnailPreview');
const photoPreviewContainer = document.getElementById('photoPreviewContainer');
const thumbnailPreviewContainer = document.getElementById('thumbnailPreviewContainer');

function renderTable(items) {
    mediaTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.className = 'border-b border-gray-200 hover:bg-gray-100 transition duration-300';
        row.innerHTML = `
            <td class="py-3 px-6 text-left whitespace-nowrap">
                <img src="${item.type === 'photo' ? item.url : item.thumbnailUrl}" alt="${item.type === 'photo' ? 'Photo' : 'Video Thumbnail'}" class="w-20 h-20 object-cover rounded-lg shadow">
            </td>
            <td class="py-3 px-6 text-left">
                ${item.type.charAt(0).toUpperCase() + item.type.slice(1)}
            </td>
            <td class="py-3 px-6 text-center">
                <button onclick="updateItem(${item.id})" class="mr-2 text-blue-500 hover:text-blue-700 transition duration-300">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                </button>
                <button onclick="deleteItem(${item.id})" class="text-red-500 hover:text-red-700 transition duration-300">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                </button>
            </td>
        `;
        mediaTableBody.appendChild(row);
    });
}

function filterItems(type) {
    const filteredItems = type === 'all' ? mediaItems : mediaItems.filter(item => item.type === type);
    renderTable(filteredItems);
}

document.getElementById('filterAll').addEventListener('click', () => filterItems('all'));
document.getElementById('filterPhoto').addEventListener('click', () => filterItems('photo'));
document.getElementById('filterVideo').addEventListener('click', () => filterItems('video'));

mediaType.addEventListener('change', () => {
    if (mediaType.value === 'photo') {
        photoInputs.classList.remove('hidden');
        videoInputs.classList.add('hidden');
    } else {
        photoInputs.classList.add('hidden');
        videoInputs.classList.remove('hidden');
    }
});

photoUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            photoPreview.src = reader.result;
            photoPreviewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

thumbnailUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            thumbnailPreview.src = reader.result;
            thumbnailPreviewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

mediaForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const newItem = {
        id: Date.now(),
        type: mediaType.value,
    };

    if (mediaType.value === 'photo') {
        newItem.url = photoPreview.src;
    } else {
        newItem.url = URL.createObjectURL(videoUpload.files[0]);
        newItem.thumbnailUrl = thumbnailPreview.src;
    }

    mediaItems.push(newItem);
    renderTable(mediaItems);
    mediaForm.reset();
    photoPreviewContainer.classList.add('hidden');
    thumbnailPreviewContainer.classList.add('hidden');
});

function updateItem(id) {
    // Implement update logic here
    console.log('Update item:', id);
}

function deleteItem(id) {
    mediaItems = mediaItems.filter(item => item.id !== id);
    renderTable(mediaItems);
}

// Initial render
renderTable(mediaItems);