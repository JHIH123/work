<template>
  <div class="card">
    <div class="p">
      <el-button @click="showConfirmationDialog">
        <el-icon><Back /></el-icon> Back
      </el-button>
      <el-form :model="form" label-width="150px">
        <el-row :gutter="10">
          <!-- Add form fields here as needed -->
          <el-col :span="11">
            <el-form-item label="Appointment ID:">
              <el-input v-model="form.AppointmentID" :disabled="true" placeholder="New"/>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Health Center:">
              <el-input v-model="form.HealthCenter" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="InpatientID:">
              <el-input v-model="form.InpatientID" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Patient Status:">
              <el-select v-model="form.PatientStatus">
                <el-option label="Ambulatory" value="Ambulatory" />
                <!-- Add other options here -->
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Patient ID:">
              <el-input v-model="form.PatientID" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Patient Name:">
              <el-input v-model="form.PatientName" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Urgency Level:">
              <el-select v-model="form.UrgencyLevel">
                <el-option label="N" value="N" />
                <!-- Add other options here -->
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Specialty:">
              <el-input v-model="form.Specialty" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Appointment Date:">
              <el-date-picker v-model="form.AppointmentDate" type="datetime" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Status:">
              <el-input v-model="form.Status" maxlength="1" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Doctor:">
              <el-select v-model="form.Doctor">
                <el-option label="Dr.Jack" value="Dr.Jack" />
                <el-option label="Dr. Emily" value="Dr. Emily" />
                <!-- Add doctor options here -->
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Invoice Exempt:">
              <el-checkbox v-model="form.IsInvoice" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Consultation Service:">
              <el-select v-model="form.Consultation">
                <el-option label="General Consultation" value="General Consultation" />
                <el-option label="Surgery Consultation" value="Surgery Consultation" />
                <!-- Add service options here -->
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
  name: 'NewAppointments',
  components: {
    Back,
    DocumentChecked,
    Delete,
    DeleteConfirmation
  },
  data() {
    return {
      form: {
        AppointmentID: '',
        HealthCenter: '',
        InpatientID: '',
        PatientStatus: '',
        PatientID: '',
        PatientName: '',
        UrgencyLevel: '',
        AppointmentDate: '',
        Specialty: '',
        Doctor: '',
        Consultation: '',
        Status: '',
        IsInvoice: ''
      },
      confirmationDialogVisible: false
    };
  },
  created() {
    const appointmentId = this.$route.query.appointmentId;
    if (appointmentId) {
      this.fetchAppointmentDetails(appointmentId);
    }
  },
  methods: {
    getModalWidth() {
      return window.innerWidth <= 800 ? '300px' : '500px';
    },
    // 顯示確認是否要返回的視窗
    showConfirmationDialog() {
      this.$refs.deleteConfirmation.showBackConfirmationModal();
    },
    // 定義格式化日期時間的函數
    formatDateTime(date) {
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      const hours = ('0' + date.getHours()).slice(-2);
      const minutes = ('0' + date.getMinutes()).slice(-2);
      const seconds = ('0' + date.getSeconds()).slice(-2);
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    // 處理提交
    handleSubmit() {
      // 將 IsInvoice 轉換為 'Y' 或 'N'
      this.form.IsInvoice = this.form.IsInvoice ? 'Y' : 'N';

      // 確保 AppointmentID 是 null
      if (!this.form.AppointmentID) {
        this.form.AppointmentID = null;
      }

      // 格式化日期時間字段
      if (this.form.AppointmentDate) { 
        const date = new Date(this.form.AppointmentDate);
        this.form.AppointmentDate = this.formatDateTime(date);
      }

      // 設定 API URL
      const apiUrl = this.form.AppointmentID ?
        api.domain + '/Appointment/EditAppointment' :
        api.domain + '/Appointment/EditAppointment';

      // 在發送請求之前將表單數據輸出到控制台
      console.log('提交的表單數據:', this.form);

      // 發送 API 請求
      axios
        .post(apiUrl, this.form)
        .then((response) => {
          // 成功提示
          Swal.fire({
            title: 'The record has been saved.',
            icon: 'success',
            confirmButtonText: 'Close'
          }).then(() => {
            // 返回主頁
            this.$router.push('/');
          });
        })
        .catch((error) => {
          // 錯誤提示
          Swal.fire({
            title: 'Error saving the record.',
            icon: 'error',
            confirmButtonText: 'Close'
          });
          // 輸出錯誤信息到控制台
          console.error('Error saving appointment:', error);
        });
    },
    // 刪除
    handleDelete() {
      const apiUrl = api.domain + '/Appointment/DeleteAppointmet';
      axios
        .post(apiUrl, { AppointmentID: this.form.AppointmentID })
        .then((response) => {
          Swal.fire({
            title: 'The record has been deleted.',
            icon: 'success',
            confirmButtonText: 'Close'
          })
          
        })
        .then(() => {
            // 彈窗關閉後返回上一頁
            this.$router.back();
          })
        .catch((error) => {
          console.error('刪除預約時出錯:', error);
        })
        .catch((error) => {
          Swal.fire({
            title: 'Error deleting the record.',
            icon: 'error',
            confirmButtonText: 'Close'
          });
          console.error('Error deleting appointment:', error);
        });
    },
    // 取得預約詳情
    fetchAppointmentDetails(appointmentId) {
      axios
        .post(api.domain + '/Appointment/AppointmentInfo', { appointmentId })
        .then((response) => {
          const appointment = response.data.Data;
          if (appointment && appointment.AppointmentID === appointmentId) {
            Object.assign(this.form, appointment);
          }
        })
        .catch((error) => {
          console.error('Error fetching appointment details:', error);
        });
    },
    showDeleteModal() {
      console.log('showDeleteModal 已被啟用');
      this.$refs.deleteConfirmation.showDeleteModal(this.handleDelete);
    },
    
  },
};
</script>

<style scoped>

@media (max-width: 1024px) {
  /* 1024px 以下适用 */
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
    right: 760%;
  }
  .el-button {
    margin-top: 20px;
    margin-left: 1%;
  }
  .action-buttons {
    margin-left: 50%;
  }
}

@media (max-width: 800px) {
  /* 800px 以下适用，优先级较高 */
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
    margin-left: 15px;
    margin-bottom: 13px;
    right: 70%;
  }
  .el-button {
    margin-top: 20px;
    margin-left: 2%;
  }
  .action-buttons {
    margin-left: 30%;
  }
  .swal2-popup {
    width: 200px !important; /* 設置視窗寬度 */
    font-size: 100px; /* 調整字體大小以適應較小視窗 */
  }
}

@media (min-width: 1024px) {
  /* 1025px 以上适用 */
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
    margin-left: 69%;
  }
}


</style>