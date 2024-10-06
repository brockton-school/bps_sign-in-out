// Redirect after 2 seconds (confirmation page)
function redirectToHome() {
    setTimeout(function() {
        window.location.href = "/";
    }, 2000);
}

// Show reason field only if user is a student and signing out, and hide action buttons
function handleAction(action, userType) {
    var reasonField = document.getElementById("reason-field");
    var actionButtons = document.getElementById("action-buttons");
    var visitorReasonField = document.getElementById("visitor-reason");
    var header = document.getElementById("sign-in-out-header");

    // Set the action in the form and handle the display of the reason field
    document.getElementById('action-input').value = action;

    if (userType === "Student" && action === "Signing Out") {
        reasonField.style.display = "block";
        actionButtons.style.display = "none";  // Hide the Sign In/Out buttons
    } else if (userType === "Visitor" && action === "Signing In") {
        visitorReasonField.style.display = "block";
        actionButtons.style.display = "none";  // Hide the Sign In/Out buttons
        header.style.display = "none";
    } else {
        reasonField.style.display = "none";
        document.getElementById('reason-input').value = ""; // Clear any existing reason
        document.forms['signForm'].submit();  // Automatically submit the form
    }
}

// Function to set the reason when a reason button is clicked
function setReason(reason) {
    document.getElementById('reason-input').value = reason;
    document.forms['signForm'].submit();  // Submit form when reason is selected
}

// Function to submit the form on Enter key in the "Other reason" input
function submitOnEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevent the default form submission behavior
        const otherReason = document.getElementById('other-reason-input').value;
        setReason(otherReason);  // Set the reason and submit the form
    }
}