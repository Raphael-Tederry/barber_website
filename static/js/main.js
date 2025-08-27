// Main JavaScript functionality for the barbershop website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initBookingForm();
    initLanguageToggle();
    initAnimations();
});

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    // Add scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Language toggle functionality
function initLanguageToggle() {
    const languageToggle = document.querySelector('.language-toggle');
    if (languageToggle) {
        languageToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentLang = new URLSearchParams(window.location.search).get('lang') || 'en';
            const newLang = currentLang === 'en' ? 'he' : 'en';
            
            // Update URL with new language
            const url = new URL(window.location);
            url.searchParams.set('lang', newLang);
            window.location.href = url.toString();
        });
    }
}

// Booking form functionality
function initBookingForm() {
    const bookingForm = document.getElementById('bookingForm');
    if (!bookingForm) return;
    
    const serviceCheckboxes = document.querySelectorAll('input[name="services"]');
    const dateInput = document.getElementById('date');
    const timeSlotsContainer = document.getElementById('timeSlots');
    const selectedTimeInput = document.getElementById('selectedTime');
    
    let selectedServices = [];
    let availableSlots = [];
    
    // Service selection
    serviceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedServices();
            updateTimeSlotsIfDateSelected();
        });
    });
    
    // Date selection
    if (dateInput) {
        // Set minimum date to today
        const today = new Date();
        const maxDate = new Date(today.getTime() + (7 * 24 * 60 * 60 * 1000)); // 7 days ahead
        
        dateInput.min = today.toISOString().split('T')[0];
        dateInput.max = maxDate.toISOString().split('T')[0];
        
        dateInput.addEventListener('change', function() {
            if (this.value && selectedServices.length > 0) {
                loadAvailableSlots(this.value, selectedServices);
            } else {
                clearTimeSlots();
            }
        });
    }
    
    // Form submission
    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateBookingForm()) {
            return;
        }
        
        submitBooking();
    });
    
    function updateSelectedServices() {
        selectedServices = Array.from(serviceCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        
        // Update UI to show selected services
        serviceCheckboxes.forEach(cb => {
            const item = cb.closest('.checkbox-item');
            if (cb.checked) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
    }
    
    function updateTimeSlotsIfDateSelected() {
        if (dateInput && dateInput.value && selectedServices.length > 0) {
            loadAvailableSlots(dateInput.value, selectedServices);
        } else {
            clearTimeSlots();
        }
    }
    
    async function loadAvailableSlots(date, services) {
        if (!timeSlotsContainer) return;
        
        // Show loading
        showLoading(timeSlotsContainer);
        
        try {
            const response = await fetch(`/api/available-slots?date=${date}&services=${services.join(',')}`);
            const data = await response.json();
            
            if (response.ok) {
                displayTimeSlots(data.slots);
            } else {
                showError('Failed to load available slots: ' + data.detail);
                clearTimeSlots();
            }
        } catch (error) {
            console.error('Error loading slots:', error);
            showError('Failed to load available slots. Please try again.');
            clearTimeSlots();
        }
    }
    
    function displayTimeSlots(slots) {
        if (!timeSlotsContainer) return;
        
        timeSlotsContainer.innerHTML = '';
        
        if (slots.length === 0) {
            timeSlotsContainer.innerHTML = '<p class="text-center">No available slots for this date</p>';
            return;
        }
        
        const slotsGrid = document.createElement('div');
        slotsGrid.className = 'time-slots';
        
        slots.forEach(slot => {
            const slotElement = document.createElement('div');
            slotElement.className = 'time-slot';
            slotElement.textContent = slot;
            slotElement.addEventListener('click', function() {
                selectTimeSlot(this, slot);
            });
            slotsGrid.appendChild(slotElement);
        });
        
        timeSlotsContainer.appendChild(slotsGrid);
    }
    
    function selectTimeSlot(element, time) {
        // Remove previous selection
        document.querySelectorAll('.time-slot.selected').forEach(slot => {
            slot.classList.remove('selected');
        });
        
        // Select current slot
        element.classList.add('selected');
        if (selectedTimeInput) {
            selectedTimeInput.value = time;
        }
    }
    
    function clearTimeSlots() {
        if (timeSlotsContainer) {
            timeSlotsContainer.innerHTML = '';
        }
        if (selectedTimeInput) {
            selectedTimeInput.value = '';
        }
    }
    
    function validateBookingForm() {
        const name = document.getElementById('customerName')?.value.trim();
        const email = document.getElementById('customerEmail')?.value.trim();
        const phone = document.getElementById('customerPhone')?.value.trim();
        const date = dateInput?.value;
        const time = selectedTimeInput?.value;
        
        if (!name) {
            showError('Please enter your name');
            return false;
        }
        
        if (!email || !isValidEmail(email)) {
            showError('Please enter a valid email address');
            return false;
        }
        
        if (!phone) {
            showError('Please enter your phone number');
            return false;
        }
        
        if (selectedServices.length === 0) {
            showError('Please select at least one service');
            return false;
        }
        
        if (!date) {
            showError('Please select a date');
            return false;
        }
        
        if (!time) {
            showError('Please select a time slot');
            return false;
        }
        
        return true;
    }
    
    async function submitBooking() {
        const formData = new FormData(bookingForm);
        formData.set('services', selectedServices.join(','));
        formData.set('time', selectedTimeInput.value);
        
        // Get current language
        const lang = new URLSearchParams(window.location.search).get('lang') || 'en';
        formData.set('lang', lang);
        
        try {
            // Disable form during submission
            const submitBtn = bookingForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Booking...';
            
            const response = await fetch('/api/book-appointment', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Redirect to confirmation page
                window.location.href = `/confirm?booking_id=${data.booking_id}&lang=${lang}`;
            } else {
                showError('Booking failed: ' + data.detail);
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        } catch (error) {
            console.error('Error submitting booking:', error);
            showError('Booking failed. Please try again.');
            const submitBtn = bookingForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Book Now';
        }
    }
}

// Confirmation page functionality
function initConfirmationForm() {
    const confirmForm = document.getElementById('confirmForm');
    if (!confirmForm) return;
    
    confirmForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(confirmForm);
        
        try {
            const submitBtn = confirmForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Confirming...';
            
            const response = await fetch('/api/confirm-appointment', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showSuccess('Appointment confirmed successfully!');
                confirmForm.style.display = 'none';
            } else {
                showError('Confirmation failed: ' + data.detail);
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        } catch (error) {
            console.error('Error confirming appointment:', error);
            showError('Confirmation failed. Please try again.');
            const submitBtn = confirmForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Confirm Appointment';
        }
    });
}

// Animation functionality
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.service-card, .product-card, .contact-card, .about-content').forEach(el => {
        observer.observe(el);
    });
}

// Modal functionality
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Utility functions
function showLoading(container) {
    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading available times...</p>
        </div>
    `;
}

function showError(message) {
    // Remove existing alerts
    document.querySelectorAll('.alert').forEach(alert => alert.remove());
    
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger';
    alert.textContent = message;
    
    // Insert at top of page or form
    const target = document.querySelector('.booking-form') || document.querySelector('.container');
    if (target) {
        target.insertBefore(alert, target.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
        
        // Scroll to alert
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function showSuccess(message) {
    // Remove existing alerts
    document.querySelectorAll('.alert').forEach(alert => alert.remove());
    
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.textContent = message;
    
    const target = document.querySelector('.container');
    if (target) {
        target.insertBefore(alert, target.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
        
        // Scroll to alert
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Initialize confirmation form if on confirmation page
if (document.getElementById('confirmForm')) {
    initConfirmationForm();
}
