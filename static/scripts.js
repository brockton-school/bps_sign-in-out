// Redirect after 2 seconds (confirmation page)
function redirectToHome() {
    setTimeout(function() {
        window.location.href = "/";
    }, 2000);
}

// Show reason field if sign out or student sign in, and hide action buttons
function handleAction(action, userType) {
    var reasonField = document.getElementById("reason-field");
    var actionButtons = document.getElementById("action-buttons");
    var visitorReasonField = document.getElementById("visitor-reason");
    var header = document.getElementById("sign-in-out-header");

    // Set the action in the form and handle the display of the reason field
    document.getElementById('action-input').value = action;

    if (userType === "Student") {
        reasonField.style.display = "block";
        actionButtons.style.display = "none";  // Hide the action buttons
        if (action == "Signing In") {
            document.getElementById("reason-header").innerText = "Reason for Sign In"
        }
    } else if (userType === "Staff" && action === "Signing Out") {
        reasonField.style.display = "block";
        actionButtons.style.display = "none";  // Hide the action buttons
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

    // Get form state
    var action = document.getElementById('action-input').value
    var userType = document.getElementById('user-type-input').value

    if (action === "Signing Out" && userType !== "Visitor") {
        // Hide the reason fields
        var reasonField = document.getElementById("reason-field");
        reasonField.style.display = "none";

        // Then ask for return time...
        var returnTime = document.getElementById("return-time");
        returnTime.style.display = "block";

    } else {
        // Otherwise just submit...
        document.forms['signForm'].submit();
    }
    
}

// Function to submit the form on Enter key in the "Other reason" input
function submitOnEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevent the default form submission behavior
        const otherReason = document.getElementById('other-reason-input').value;
        setReason(otherReason);  // Set the reason and submit the form
    }
}

// Function to set the return time when button is clicked
function setReturnTime(time) {
    document.getElementById('return-time-input').value = time;
    document.forms['signForm'].submit();
}

function submitTimeOnEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevent the default form submission behavior
        const otherTime = document.getElementById('return-time-input').value;
        setReturnTime(otherTime);  // Set the time and submit the form
    }
}

// Handle visitor info submission
function submitVisitorOnEnter(event) {
    if (event.key === "Enter") {
        document.forms['signForm'].submit();
    }
}