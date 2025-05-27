<template>
    <div v-if="visible" class="search-window">
      <div class="search-window-content">
        <button @click="close">X</button>
        <form @submit.prevent="search">
          <label for="appointmentId">Appointment ID:</label>
          <input type="text" id="appointmentId" v-model="appointmentId">
          <label for="patientName">Patient Name:</label>
          <input type="text" id="patientName" v-model="patientName">
          <label for="date">Date:</label>
          <input type="date" id="date" v-model="date">
          <label for="doctor">Doctor:</label>
          <input type="text" id="doctor" v-model="doctor">
          <label for="specialty">Specialty:</label>
          <input type="text" id="specialty" v-model="specialty">
          <button type="submit">Search</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['visible'],
    data() {
      return {
        appointmentId: '',
        patientName: '',
        date: '',
        doctor: '',
        specialty: ''
      };
    },
    methods: {
      close() {
        this.$emit('close');
      },
      search() {
        this.$emit('search', {
          appointmentId: this.appointmentId,
          patientName: this.patientName,
          date: this.date,
          doctor: this.doctor,
          specialty: this.specialty
        });
      }
    }
  };
  </script>
  
  <style>
  .search-window {
    position: fixed;
    top: 0;
    right: 0;
    width: 30%;
    height: 100%;
    background-color: rgb(255, 255, 255);
    box-shadow: -2px 0 5px rgba(0,0,0,0.5);
    z-index: 1000;
    transition: transform 0.3s ease-in-out;
  }
  
  .search-window-content {
    padding: 20px;
  }
  
  .search-window button {
    background-color: rgb(100, 119, 237);
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
  }
  </style>
  