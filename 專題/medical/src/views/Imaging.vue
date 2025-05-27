<template>
    <div class="dashboard">
      <el-card class="card">
        <div class="header">
          <el-button type="primary" @click="openSearchDialog">
            <el-icon><Search /></el-icon>
            Search
          </el-button>
          <el-button type="success" @click="$router.push('/NewImaging')">
            <el-icon><Plus /></el-icon>
            New
          </el-button>
        </div>
        <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop="ImagingID" label="ImagingID" width="160" sortable="custom"></el-table-column>
          <el-table-column prop="TestDate" label="TestDate" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="Test" label="Test" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="Urgent" label="Urgent" width="180" sortable="custom"></el-table-column>
          <el-table-column label="Operations" width="145">
            <template #default="scope">
              <el-icon @click="AppointmentsEdit(scope.row)" size="small">
                <Edit />
              </el-icon>
              <el-icon @click="handleDelete(scope.$index, scope.row.AppointmentID)" size="small">
                <Delete />
              </el-icon>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
  
      <!-- Imaging 搜索視窗 -->
      <el-dialog title="Search Imaging" v-model="searchDialogVisible" width="50%">
        <el-form :model="searchForm" label-width="120px">
          <el-form-item label="Imaging ID:">
            <el-input v-model="searchForm.ImagingID" placeholder="Please enter an Imaging ID"></el-input>
          </el-form-item>
          <el-form-item label="Test Date:">
            <el-date-picker
                v-model="searchForm.TestDate"
                type="date"
                placeholder="Please enter a Test Date"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                style="width: 100%;"
            ></el-date-picker>
          </el-form-item>
          <el-form-item label="Test:">
            <el-input v-model="searchForm.Test" placeholder="Please enter an Patient ID"></el-input>
          </el-form-item>
          <el-form-item label="Patient ID:">
            <el-input v-model="searchForm.PatientID" placeholder="Please enter an Patient ID"></el-input>
          </el-form-item>
          <el-form-item label="Physician:">
            <el-input v-model="searchForm.Physician" placeholder="Please enter a Physician"></el-input>
          </el-form-item>
          <el-form-item label="Urgent:">
            <el-checkbox-group v-model="searchForm.Urgent">
                <el-checkbox label="Y">Y</el-checkbox>
            </el-checkbox-group>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="resetSearchForm">Reset</el-button>
          <el-button type="primary" @click="searchAppointments">Search</el-button>
        </span>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import { Edit, Delete, Plus, Search } from '@element-plus/icons-vue';
  import * as api from '../api/api.js';
  import axios from 'axios';
  
  export default {
    name: 'Imaging',
    components: {
      Edit,
      Delete,
      Plus,
      Search,
    },
    data() {
      return {
        activeTab: 'Imaging',
        searchDialogVisible: false,
        searchForm: {
          ImagingID: '',
          TestDate: '',
          Test: '',
          PatientStatus: '',
          PatientID: '',
          Physician: '',
          Urgent: '',
        },
        tableData: [],
      };
    },
    created() {
      this.fetchImaging();
    },
    methods: {
      //搜尋開關編輯方法
      openSearchDialog() {
        this.searchDialogVisible = true;
      },
      //Imaging編輯方法
      ImagingEdit(row) {
        this.$router.push({ name: 'NewImaging', query: { appointmentId: row.AppointmentID } });
        console.log('Editing appointment with ID:', row.AppointmentID);
      },
      //Diagnosis編輯方法
      DiagnosisEdit(row) {
        this.$router.push({ name: 'NewDiagnosis', query: { appointmentid: row.AppointmentID } });
        console.log('Editing appointment with ID:', row.AppointmentID);
      },
      resetSearchForm() {
        this.searchForm = {
          ImagingID: '',
          TestDate: '',
          Test: '',
          PatientStatus: '',
          PatientID: '',
          Physician: '',
          Urgent: '',
        };
      },
      //搜尋資料
      searchImaging() {
        const { appointmentId, patientName, urgencyLevel, date, doctor, speciality } = this.searchForm;
        axios
          .post(api.domain + '/Appointment/AppointmentList', {
            AppointmentID: appointmentId,
            PatientName: patientName,
            UrgencyLevel: urgencyLevel,
            AppointmentDate: date,
            Doctor: doctor,
            Specialty: speciality,
          })
          .then((response) => {
            console.log('Response data:', response.data);
            if (response.data && response.data.Data) {
              this.tableData = response.data.Data;
              this.searchDialogVisible = false;
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching appointments:', error);
          });
      },
      //取得資料顯示在畫面上
      fetchImaging() {
        axios
          .post(api.domain + '/Appointment/AppointmentList', {})
          .then((response) => {
            console.log('Response data:', response.data);
            if (response.data && response.data.Data) {
              this.tableData = response.data.Data;
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching appointments:', error);
          });
      },
      handleEdit(index, row) {
        console.log('Edit:', index, row);
      },
      //刪除資料
      ImagingDelete(index, AppointmentID) {
        axios
          .post(api.domain + '/Appointment/DeleteAppointmet', {
            AppointmentID: AppointmentID})
          .then((response) => {
            console.log('刪除回應:', response.data);
            // 更新tableData刪除已刪除的預約
            this.tableData.splice(index, 1);
          })
          .catch((error) => {
            console.error('刪除預約時出錯:', error);
          });
      },
      //排序
      handleSortChange({ column, prop, order }) {
        this.tableData.sort((a, b) => {
          if (order === 'ascending') {
            return a[prop] > b[prop] ? 1 : -1;
          } else {
            return a[prop] < b[prop] ? 1 : -1;
          }
        });
      },
      handleTabClick(tab) {
        console.log('Tab clicked:', tab);
      },
    },
  };
  </script>
  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px; /* 按鈕跟欄位的間距 */
  }
  
  .card {
    background-color: #eaf5fc;
    border-radius: 30px; /* 切角 */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
  
  .el-table {
    border-radius: 20px; /* 切角 */
  }
  
  .el-icon {
    margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  </style>
  