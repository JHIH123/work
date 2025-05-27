<template>
  <div class="dashboard">
    <el-card class="card">
      <div class="header">
        <el-button type="primary" @click="openSearchDialog">
          <el-icon><Search /></el-icon>
          Search
        </el-button>
        <el-button type="success" @click="$router.push('/NewAppointments')">
          <el-icon><Plus /></el-icon>
          New
        </el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
        <el-table-column prop="AppointmentID" label="Appointment ID" width="160" sortable="custom"></el-table-column>
        <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
        <el-table-column prop="PatientName" label="Patient Name" width="150" sortable="custom"></el-table-column>
        <el-table-column prop="UrgencyLevel" label="Urgency Level" width="150" sortable="custom"></el-table-column>
        <el-table-column prop="AppointmentDate" label="Appointment Date" width="180" sortable="custom"></el-table-column>
        <el-table-column prop="Specialty" label="Specialty" width="140" sortable="custom"></el-table-column>
        <el-table-column prop="Doctor" label="Doctor" width="130" sortable="custom"></el-table-column>
        <el-table-column label="Operations" width="145">
          <template #default="scope">
            <el-icon @click="DiagnosisEdit(scope.row)" size="small">
              <Memo />
            </el-icon>
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

    <!-- Search Dialog -->
    <el-dialog title="Search Appointments" v-model="searchDialogVisible" width="50%">
      <el-form :model="searchForm" label-width="120px">
        <el-form-item label="Appointment ID">
          <el-input v-model="searchForm.appointmentId" placeholder="Please enter an Appointment ID"></el-input>
        </el-form-item>
        <el-form-item label="Patient Name">
          <el-input v-model="searchForm.patientName" placeholder="Please enter a Patient Name"></el-input>
        </el-form-item>
        <el-form-item label="Date">
          <el-date-picker v-model="searchForm.Date" type="date" placeholder="Please enter an Appointment Date" style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="Doctor">
          <el-input v-model="searchForm.doctor" placeholder="Please enter a Doctor"></el-input>
        </el-form-item>
        <el-form-item label="Speciality">
          <el-input v-model="searchForm.speciality" placeholder="Please enter a Specialty"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetSearchForm">Reset</el-button>
        <el-button type="primary" @click="searchAppointments">Search</el-button>
      </span>
    </el-dialog>
    <!-- 确保 DeleteConfirmation 组件已正确引用 -->
    <DeleteConfirmation ref="deleteConfirmation" />
  </div>
</template>

<script>
import { Edit, Delete, Plus, Search } from '@element-plus/icons-vue';
import DeleteConfirmation from '../components/DeleteConfirmation.vue';
import dayjs from 'dayjs';
import * as api from '../api/api.js';
import axios from 'axios';

export default {
  name: 'Appointments',
  components: {
    Edit,
    Delete,
    Plus,
    Search,
    DeleteConfirmation,
  },
  data() {
    return {
      activeTab: 'Appointments',
      searchDialogVisible: false,
      searchForm: {
        AppointmentID: '',
        HealthCenter: '',
        InpatientID: '',
        PatientStatus: '',
        PatientID: '',
        PatientName: '',
        UrgencyLevel: '',
        Date: '',
        Specialty: '',
        Doctor: '',
        Consultation: '',
        Status: '',
        IsInvoice: ''
      },
      tableData: [],
    };
  },
  created() {
    this.fetchAppointments();
  },
  methods: {
    //搜尋開關編輯方法
    openSearchDialog() {
      this.searchDialogVisible = true;
    },
    //Appointments編輯方法
    AppointmentsEdit(row) {
      this.$router.push({ name: 'NewAppointments', query: { appointmentId: row.AppointmentID } });
      console.log('Editing appointment with ID:', row.AppointmentID);
    },
    //Diagnosis編輯方法
    DiagnosisEdit(row) {
      this.$router.push({ name: 'NewDiagnosis', query: { appointmentid: row.AppointmentID } });
      console.log('Editing appointment with ID:', row.AppointmentID);
    },
    resetSearchForm() {
      this.searchForm = {
        AppointmentID: '',
        HealthCenter: '',
        InpatientID: '',
        PatientStatus: '',
        PatientID: '',
        PatientName: '',
        UrgencyLevel: '',
        Date: '',
        Specialty: '',
        Doctor: '',
        Consultation: '',
        Status: '',
        IsInvoice: ''
      };
    },
    //搜尋資料
    searchAppointments() {
      // 格式化日期
      const formattedDate = this.searchForm.Date
        ? dayjs(this.searchForm.Date).format('YYYY-MM-DD HH:mm:ss') // 添加时间部分
        : ''; // 如果日期为空，传递空字符串

      console.log('Sending search params:', {
        AppointmentID: this.searchForm.AppointmentID,
        PatientName: this.searchForm.PatientName,
        UrgencyLevel: this.searchForm.UrgencyLevel,
        Date: formattedDate,
        Doctor: this.searchForm.Doctor,
        Specialty: this.searchForm.Specialty,
      });

      axios
        .post(api.domain + '/Appointment/AppointmentList', {
          AppointmentID: this.searchForm.AppointmentID,
          PatientName: this.searchForm.PatientName,
          UrgencyLevel: this.searchForm.UrgencyLevel,
          Date: formattedDate,
          Doctor: this.searchForm.Doctor,
          Specialty: this.searchForm.Specialty,
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
    fetchAppointments() {
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
    AppointmentsDelete(index, AppointmentID) {
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
    handleDelete(index, AppointmentID) {
      console.log('Deleting appointment with ID:', AppointmentID);
      this.$refs.deleteConfirmation.showDeleteModal(() => {
        this.AppointmentsDelete(index, AppointmentID);
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
@media (max-width: 800px) {
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px; /* 按鈕跟欄位的間距 */
}
.card {
  background-color: #eaf5fc;
  border-radius: 3cqmin; /* 切角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
} 
.el-table {
  border-radius: 20px; /* 切角 */
}

.el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
}
.dialog-footer{
  margin-right: 10px; /* 修改跟刪除icon的距離 */
}
}

@media (max-width: 1024px) {
.header {
 display: flex;
 justify-content: space-between;
 margin-bottom: 10px; /* 按鈕跟欄位的間距 */
}
.card {
  background-color: #eaf5fc;
  border-radius: 3cqmin; /* 切角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
} 
.el-table {
  border-radius: 20px; /* 切角 */
}

.el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
}
.dialog-footer{
  margin-right: 10px; /* 修改跟刪除icon的距離 */
}
}

@media (min-width: 1080px) {
.header {
 display: flex;
 justify-content: space-between;
 margin-bottom: 10px; 
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
}

</style>
