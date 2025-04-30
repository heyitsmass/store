const modal = document.getElementById("editModal");
const editForm = document.getElementById("editForm");
let currentEditId = null;

// Toggle database status
async function toggleDatabaseStatus(id, isActive) {
	try {
		const response = await fetch(`/api/databases/${id}`, {
			method: "PATCH",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ status: isActive ? "active" : "inactive" }),
		});
		if (response.ok) {
			location.reload(); // Refresh the page to reflect changes
		} else {
			console.error("Failed to update database status");
			// Revert the toggle if the update failed
			const checkbox = document.querySelector(`input[onchange*="toggleDatabaseStatus(${id},"]`);
			if (checkbox) checkbox.checked = !isActive;
		}
	} catch (error) {
		console.error("Error toggling database status:", error);
	}
}

// Open the edit modal
async function openModal(id) {
	currentEditId = id;
	try {
		const response = await fetch(`/api/databases/${id}`);
		const db = await response.json();
		document.getElementById("dbId").value = db.id;
		document.getElementById("dbName").value = db.name;
		document.getElementById("dbAddress").value = db.address;
		document.getElementById("dbStatus").value = db.status;
		modal.showModal();
	} catch (error) {
		console.error("Error fetching database details:", error);
	}
}

// Close the modal
function closeModal() {
	modal.close();
	editForm.reset();
}

// Handle form submission
editForm.addEventListener("submit", async (e) => {
	e.preventDefault();
	const formData = new FormData(editForm);
	const updatedDb = Object.fromEntries(formData.entries());

	try {
		const response = await fetch(`/api/databases/${currentEditId}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(updatedDb),
		});
		if (response.ok) {
			closeModal();
			location.reload(); // Refresh the page to reflect changes
		} else {
			console.error("Failed to update database");
		}
	} catch (error) {
		console.error("Error updating database:", error);
	}
});

// Close the modal if the user clicks outside of it
modal.addEventListener("click", (e) => {
	const dialogDimensions = modal.getBoundingClientRect();
	if (
		e.clientX < dialogDimensions.left ||
		e.clientX > dialogDimensions.right ||
		e.clientY < dialogDimensions.top ||
		e.clientY > dialogDimensions.bottom
	) {
		closeModal();
	}
});
