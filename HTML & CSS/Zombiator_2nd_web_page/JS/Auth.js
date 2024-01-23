// Function to handle login
function handleLogin() {
    // Retrieve the email and password input values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Perform login validation or send data to the server for authentication
    // Replace this with your login logic

    // For demonstration purposes, logging the input values
    console.log('Email:', email);
    console.log('Password:', password);

  // Input validation: Check if email or password is empty
  if (!email || !password) {
       displayNotification('Email and password are required!', 'danger',2000);
    return;
  }

  // Validate email format using a regular expression
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
      displayNotification('Please enter a valid email address!', 'danger',2000);
    return;
  }

  // Preparing data
  var data = {
    email: email,
    password: password
  };

  // Making the POST request
  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    return response.json();
  })
  .then(data => {
    if (data.status === 1) {
      displayNotification(data.message,'success',2000); // Logged in successfully or new player created
      window.location.href = "/"; // Redirect to '/game'
    } else {
      displayNotification(data.message,'danger',2000); // Show error message
    }
  })
  .catch(error => {
    console.error("There was a problem with the fetch operation:", error);
    displayNotification("An error occurred. Please try again later.",'danger',2000); // Generic error message
  });

    // You can add your login logic here, such as making an API call or any other operation related to login.
}

// Event listener when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function() {
    const loginImage = document.getElementById('loginImage');

    loginImage.addEventListener('click', function() {
        handleLogin();
    });
});

function displayNotification(message, type, duration = 3000) {
    const notificationContainer = document.getElementById('notificationContainer');
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    notification.setAttribute('role', 'alert');
    notification.innerHTML = `
        <strong>${message}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    notificationContainer.appendChild(notification);

    setTimeout(() => {
        notificationContainer.removeChild(notification);
    }, duration);
}
(() => {
    const gameStart = async () => {
        const emailInput = document.querySelector('.email');
        const passwordInput = document.querySelector('.password');

        if (emailInput.value.length === 0) {
            displayNotification('Email cannot be empty', 'danger');
            return;
        }

        // Validate email
        if (!validateEmail(emailInput.value)) {
            displayNotification('Please enter a valid email address', 'danger');
            return;
        }

        // Validate password
        if (passwordInput.value.length === 0) {
            displayNotification('Password cannot be empty', 'danger');
            return;
        }

        const url = 'http://127.0.0.1:5000/login';
        const data = {
            email: emailInput.value,
            password: passwordInput.value
        };

        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to authenticate player');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                displayNotification(responseData.message, 'danger');
                return;
            }

            $('#loadingModal').modal('show');

            window.location.href = '/game';
        } catch (error) {
            console.error(error);
        }
    };

    const validateEmail = (email) => {
        const emailRegex = /\S+@\S+\.\S+/;
        return emailRegex.test(email);
    };

    const init = () => {
        // Keyup enter event listener
        document.querySelector('.email').addEventListener('keyup', (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                gameStart();
            }
        });

        // Keyup enter event listener
        document.querySelector('.password').addEventListener('keyup', (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                gameStart();
            }
        });

        // Add event listener to start game button
        document.querySelector('.start-game-button').addEventListener('click', gameStart);
    };

    init();
})();
