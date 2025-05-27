<template>
    <div class="card">
      <div class="p">
        <el-button @click="showConfirmationDialog">
          <el-icon><Back /></el-icon> Back
        </el-button>
        
        <el-form :model="form" label-width="190px">
          <el-row :gutter="10">
            <!-- Existing form fields -->
            <el-col :span="11">
              <el-form-item label="InpatientID:" >
                <el-input v-model="form.InpatientID" placeholder="New" :disabled="true"/>
              </el-form-item>
            </el-col>
            <el-col :span="11"></el-col>

            <el-col :span="11">
              <el-form-item label="Patient ID:">
                <el-input v-model="form.PatientID" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Patient Name:">
                <el-input v-model="form.PatientName" :disabled="true"/>
              </el-form-item>
            </el-col>

            <el-col :span="11">
              <el-form-item label="Hospitalization date:">
                <el-date-picker
                  v-model="form.HospitalDate"
                  type="date"/>
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Expected Discharge date:">
              <el-date-picker v-model="form.DischargedDate" type="date"/>
                
            </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Admission type:">
                <el-select v-model="form.AdmissionType">
                  <el-option label="Emergency" value="Emergency" />
                  <!-- Add other options here -->
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Hospital Bed:">
                <el-select v-model="form.HospitalBed">
                  <el-option label="B101" value="B101" />
                  <el-option label="A104" value="A104" />
                  <!-- Add other options here -->
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="11">
                <el-form-item label="IsPaid:">
                <!-- <el-checkbox v-model="form.IsPaid" maxlength="1"/>-->
                <el-select v-model="form.IsPaid">
                  <el-option label="N" value="N" />
                  <el-option label="Y" value="Y" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        
  
          <el-form-item class="action-buttons">
            <el-button type="primary" @click="handleSubmit">
              <el-icon><DocumentChecked /></el-icon> Save
            </el-button>
            <el-button type="danger" @click="showDeleteModal">
              <el-icon><Delete /></el-icon> Delete
            </el-button>
          </el-form-item>
        </el-form>
        <DeleteConfirmation ref="deleteConfirmation" @confirmed-delete="handleDelete" />
      </div>
    </div>
  </template>
    
  <script>
    import { Back, DocumentChecked, Delete } from '@element-plus/icons-vue';
    import DeleteConfirmation from '../components/DeleteConfirmation.vue';
    import * as api from '../api/api.js';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    
    
  
    export default {
      name: 'NewInpatient',
      components: {
        Back,
        DocumentChecked,
        Delete,
        DeleteConfirmation,
      },
      data() {
        return {
          form: {
            "InpatientID": null,
            "PatientID": '',
            "PatientName":'',
            "HospitalDate": '',
            "DischargedDate": '',
            "AdmissionType": '',
            "HospitalBed": '',
            "IsPaid": '',
          }
        };
      },
      created() {
        const InpatientID = this.$route.query.InpatientID;
        if (InpatientID) {
          this.fetchInpatientDetails(InpatientID);
        }
      },
      methods: {
      // 顯示確認視窗
      showConfirmationDialog() {
        this.$refs.deleteConfirmation.showBackConfirmationModal();
      },
      showDeleteModal() {
        console.log('showDeleteModal 已被啟用');
        if (this.$refs.deleteConfirmation && this.$refs.deleteConfirmation.showDeleteModal) {
          this.$refs.deleteConfirmation.showDeleteModal(this.handleDelete);
        } else {
          console.error('DeleteConfirmation component or method not found.');
        }
      },
      // 取得資料
      fetchInpatientDetails(InpatientID) {
        axios
          .post(api.domain + '/Inpatient/InpatientInfo', { InpatientID })
          .then((response) => {
            const Inpatient = response.data.Data;
            if (Inpatient && Inpatient.InpatientID === InpatientID) {
              Object.assign(this.form, Inpatient);
            }
          })
          .catch((error) => {
            console.error('Error fetching Inpatient details:', error);
          });
      },
      // 新增、修改資料
      handleSubmit() {
      
        function formatDateTime(date) {
          const d = new Date(date);
          const yyyy = d.getFullYear();
          const mm = String(d.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
          const dd = String(d.getDate()).padStart(2, '0');
          const hh = String(d.getHours()).padStart(2, '0');
          const min = String(d.getMinutes()).padStart(2, '0');
          const ss = String(d.getSeconds()).padStart(2, '0');
          return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
        }

        // 格式化 HospitalDate 和 DischargedDate
        this.form.HospitalDate = formatDateTime(this.form.HospitalDate);
        this.form.DischargedDate = formatDateTime(this.form.DischargedDate);


      // 檢查 InpatientID 是否為 null 來判斷是新增還是修改
      if (this.form.InpatientID !== null) {
        // 修改資料
        axios
          .post(api.domain + '/Inpatient/EditPatient', this.form)
          .then((response) => {
            Swal.fire({
              title: 'The record has been updated.',
              icon: 'success',
              confirmButtonText: 'Close'
            })
            .then(() => {
              this.$router.back();
            });
          })
          .catch((error) => {
            Swal.fire({
              title: 'Error updating the record.',
              icon: 'error',
              confirmButtonText: 'Close'
            });
            console.error('Error updating patient:', error);
          });
      } else {
        // 新增資料
        axios
          .post(api.domain + '/Inpatient/EditPatient', this.form) 
          .then((response) => {
            Swal.fire({
              title: 'The record has been added.',
              icon: 'success',
              confirmButtonText: 'Close'
            })
            .then(() => {
              this.$router.back();
            });
            console.log('data資料:', this.form);
          })
          .catch((error) => {
            Swal.fire({
              title: 'Error adding the record.',
              icon: 'error',
              confirmButtonText: 'Close'
            });
            console.error('Error adding patient:', error);
          });
      }
    },
      // 刪除
      handleDelete() {
        const apiUrl = api.domain + '/Inpatient/DeleteInpatient';
        axios
          .post(apiUrl, { InpatientID: this.form.InpatientID })
          .then((response) => {
            Swal.fire({
              title: 'The record has been deleted.',
              icon: 'success',
              confirmButtonText: 'Close'
            })
          })
          
          .catch((error) => {
            Swal.fire({
              title: 'Error deleting the record.',
              icon: 'error',
              confirmButtonText: 'Close'
            });
            console.error('Error deleting appointment:', error);
          })
          .then(() => {
            // 彈窗關閉後返回上一頁
            this.$router.back();
          })
      },
        
      }
    };
  </script>
    
  <style scoped>

  
  @media (max-width: 1024px) {
    .card {
      background-color: #eaf5fc;
      border-radius: 30px;
      padding: 15px;
      width: auto;
      box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .p {
      background-color: #ffffff;
      border-radius: 30px;
    }
    .el-form-item {
      margin-left: 0px;
      margin-bottom: 10px;
      right: 70%;
    }
    .el-button {
      margin-top: 20px;
      margin-left: 1%;
    }
    .action-buttons {
      margin-left: 44%;
    }
    .flex-container {
      display: flex;
      gap: 10px; /* Adjust gap between the select elements as needed */
    }
    .el-icon {
    margin-right: 10px; /* 修改跟刪除icon的距離 */
    }
  }
  @media (max-width: 800px) {
    .card {
      background-color: #eaf5fc;
      border-radius: 30px;
      padding: 15px;
      width: auto;
      box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .p {
      background-color: #ffffff;
      border-radius: 30px;
    }
    .el-form-item {
      margin-left: -23px;
      margin-bottom: 10px;
      right: 70%;
    }
    .el-button {
      margin-top: 20px;
      margin-left: 1%;
    }
    .action-buttons {
      margin-left: 20%;
    }
    .flex-container {
      display: flex;
      gap: 10px; /* Adjust gap between the select elements as needed */
    }
    .el-icon {
    margin-right: 10px; /* 修改跟刪除icon的距離 */
    }
    
  }
  @media (min-width: 1024px) {

    .card {
      background-color: #eaf5fc;
      border-radius: 30px;
      padding: 15px;
      width: auto;
      box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .p {
      background-color: #ffffff;
      border-radius: 30px;
    }
    .el-form-item {
      margin-left: 50px;
      margin-bottom: 12px;
      right: 70%;
    }
    .el-button {
      margin-top: 20px;
      margin-left: 1%;
    }
    .action-buttons {
      margin-left: 65%;
    }
    .flex-container {
      display: flex;
      gap: 10px; /* Adjust gap between the select elements as needed */
    }
    .el-icon {
    margin-right: 10px; /* 修改跟刪除icon的距離 */
    }
  }
 
  </style>