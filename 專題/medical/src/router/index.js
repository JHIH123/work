import { createRouter, createWebHistory } from 'vue-router';
import Appointments from '../views/Appointments.vue';
import NewAppointments from '../views/NewAppointments.vue';
import Patients from '../views/Patients.vue';
import NewPatients from '../views/NewPatients.vue';
import Inpatients from '../views/Inpatients.vue';
import NewFamily from '../views/NewFamily.vue';
import NewDiagnosis from '../views/NewDiagnosis.vue';
import NewInpatient from '../views/NewInpatient.vue';
import Prescription from '../views/Prescription.vue';
import NewPrescription from '../views/NewPrescription.vue';
import LabTests from '../views/LabTests.vue';
import Imaging from '../views/Imaging.vue';
import NewImaging from '../views/NewImaging.vue';
import Statistics from '../views/Statistics.vue';
import Analysis from '../views/Analysis.vue';

const routes = [
  {
    path: '/',
    name: 'Appointments',
    component: Appointments
  },
  {
    path: '/newappointments',
    name: 'NewAppointments',
    component: NewAppointments
  },
  {
    path: '/patients',
    name: 'Patients',
    component: Patients
  },
  {
    path: '/newpatients',
    name: 'NewPatients',
    component: NewPatients
  },
  {
    path: '/newfamily',
    name: 'NewFamily',
    component: NewFamily
  },
  {
    path: '/inpatients',
    name: 'Inpatients',
    component: Inpatients
  },
  {
    path: '/newdiagnosis',
    name: 'NewDiagnosis',
    component: NewDiagnosis
  },
  {
    path: '/newinpatient',
    name: 'NewInpatient',
    component: NewInpatient
  },
  {
    path: '/prescription',
    name: 'Prescription',
    component: Prescription
  },
  {
    path: '/newprescription',
    name: 'NewPrescription',
    component: NewPrescription
  },
  {
    path: '/labtests',
    name: 'LabTests',
    component: LabTests
  },
  {
    path: '/imaging',
    name: 'Imaging',
    component: Imaging
  },
  {
    path: '/newimaging',
    name: 'NewImaging',
    component: NewImaging
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis
  },


  
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes
});

export default router;
