<template>
  <div class="card">
    <div class="p">
      <el-button class="ButtonBack" @click="showConfirmationDialog">
        <el-icon><Back /></el-icon> Back
      </el-button>
      
      <el-form :model="form" label-width="200px">
        <el-row :gutter="10">
          <!-- Existing form fields -->
          <el-col :span="11">
            <el-form-item label="PatientID:">
              <el-input v-model="form.PatientID" placeholder="New" :disabled="true"/>
            </el-form-item>
          </el-col>
          <el-col :span="11"></el-col>
          
          <el-col :span="11">
            <el-form-item label="Patient Name:">
              <el-input v-model="form.PatientName" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Sex:">
              <el-select v-model="form.Sex" maxlength="1" >
                <el-option label="M" value="M" />
                <el-option label="F" value="F" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="ID Number:">
              <el-input v-model="form.IDNumber" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Nationality:">
              <el-select v-model="form.Nationality">
                <el-option label="Taiwan" value="Taiwan" />
                <!-- Add other options here -->
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Date of Birth:">
              <el-date-picker v-model="form.Birthday" type="date" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Patient Age:">
              <el-input v-model="form.Age" placeholder="No DoB!" :disabled="true"/>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Phone No:">
              <el-input v-model="form.PhoneNo" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Primary Care Doctor:">
              <el-select v-model="form.PrimaryCare">
                <el-option label="DR00001" value="DR00001" />
                <!-- Add other options here -->
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Hospital Status:">
              <el-select v-model="form.HospitalStatus" >
                <el-option label="N" value="N" />
                <el-option label="T" value="T" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Deceased:">
              <el-select v-model="form.IsDeceased" >
                <el-option label="N" value="N" />
                <el-option label="T" value="T" />
              </el-select>
            </el-form-item>
          </el-col>
          
          
          <el-col :span="20">
            <el-form-item label="Address:">
              <el-input type="textarea" v-model="form.Address" class="large-textarea" />
            </el-form-item>
          </el-col>
          <el-col :span="20">
            <el-form-item label="Patient Information:">
              <el-input type="textarea" v-model="form.Note" class="large-textarea" />
            </el-form-item>
          </el-col>

          <!-- Families section -->
          <el-col>
            <el-form-item label="Families">
              <el-table :data="form.Families">
                <el-table-column prop="FamilyName" label="Name"></el-table-column>
                <el-table-column prop="Relationship" label="Relationship"></el-table-column>
                <el-table-column prop="PhoneNo" label="Phone No"></el-table-column>
                <el-table-column prop="Tel" label="TEL"></el-table-column>
                <el-table-column prop="Company" label="Company" ></el-table-column>
                <el-table-column label="Operations" >
                  <template #default="scope">
                    <el-icon @click="FamilyEdit(scope.row)" size="small">
                      <Edit />
                    </el-icon>
                    <el-icon @click="confirmDeleteFamily(scope.$index, scope.row.SeqNo)" size="small">
                      <Delete />
                    </el-icon>
                  </template>
                </el-table-column>
              </el-table>
            </el-form-item>
          </el-col>
        </el-row>
      
        <div class="buttons">
          <el-form-item class="action-buttons">
            <el-button type="primary" @click="handleSubmit">
              <el-icon><DocumentChecked /></el-icon> Save
            </el-button>
            <el-button type="danger" @click="confirmDelete">
              <el-icon><Delete /></el-icon> Delete
            </el-button>
          </el-form-item>
        </div>

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
    name: 'NewPatients',
    components: {
      Back,
      DocumentChecked,
      Delete,
      DeleteConfirmation
    },
    data() {
      return {
        form: {
          "PatientID": null,
          "PatientName": '',
          "IDNumber": '',
          "Sex": '',
          "Birthday": '',
          "Age": 0,
          "Nationality": '',
          "Address": '',
          "PhoneNo": '',
          "HospitalStatus": '',
          "PrimaryCare": '',
          "IsDeceased": '',
          "Note": '',
          "Families": [
            {
              "SeqNo": '',
              "FamilyName": '',
              "Relationship": '',
              "PatientID": '',
              "Tel": '',
              "PhoneNo": '',
              "Company": ''
            }
          ]

        },
        tableData: []
      };
    },
    created() {
      const patientId = this.$route.query.patientID;
      if (patientId) {
        this.fetchPatientDetails(patientId);
      }
    },
    methods: {
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
      // 顯示確認視窗
      showConfirmationDialog() {
        this.$refs.deleteConfirmation.showBackConfirmationModal();
      },
      //資料傳遞Family
      FamilyEdit(row) {
        this.$router.push({ name: 'NewFamily', query: { seqNo: row.SeqNo } });
        console.log('Editing family with SeqNo:', row.SeqNo);
      },
      //新增
      handleSubmit() {
        console.log('Submitting form data:', this.form); // 添加调试信息
        const BD = new Date(this.form.Birthday);
        this.form.Birthday = this.formatDateTime(BD);
        console.log('查看生日:', this.form.Birthday);
        // 檢查 PatientID 來判斷是新增還是修改
        if (this.form.PatientID) {
          // 修改資料
          axios
            .post(api.domain + '/Patient/EditPatient', this.form)
            .then((response) => {
              Swal.fire({
                title: 'The record has been updated.',
                icon: 'success',
                confirmButtonText: 'Close'
              }).then(() => {
                // 彈窗關閉後返回上一頁
                this.$router.back();
              });
              console.log('編輯的data資料:', this.form);
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
            .post(api.domain + '/Patient/EditPatient', this.form)
            .then((response) => {
              Swal.fire({
                title: 'The record has been added.',
                icon: 'success',
                confirmButtonText: 'Close'
              }).then(() => {
                this.$router.back();
              });
              console.log('新增的data資料:', this.form);
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
      confirmDeleteFamily(index, SeqNo) {
        this.deleteIndex = index;
        this.deleteSeqNo = SeqNo;
        this.showDeleteModal(() => this.handleDeleteFamily());
      },
      confirmDelete() {
        this.showDeleteModal(() => this.handleDelete());
      },
      showDeleteModal(callback) {
        console.log('showDeleteModal 已被啟用');
        if (this.$refs.deleteConfirmation && this.$refs.deleteConfirmation.showDeleteModal) {
            this.$refs.deleteConfirmation.showDeleteModal(callback);
        } else {
            console.error('DeleteConfirmation component or method not found.');
        }
      },
      // 刪除資料 Patient
      handleDelete() {
        axios
          .post(api.domain + '/Patient/DeletePatient', {
            PatientID: this.form.PatientID,
          })
          .then((response) => {
            console.log('刪除回應:', response.data);
            console.log('data資料:', this.form);
            this.tableData.splice(this.deleteIndex, 1);
          })
          .then(() => {
            // 彈窗關閉後返回上一頁
            this.$router.back();
          })
          .catch((error) => {
            console.error('刪除預約時出錯:', error);
          });
      },
      // 刪除資料 Family
      handleDeleteFamily() {
        console.log('查看：',this.deleteSeqNo);
        axios
          .post(api.domain + '/Family/DeleteFamily', {
            SeqNo: this.deleteSeqNo,
          })
          .then((response) => {
            console.log('删除响应:', response.data);
            this.form.Families.splice(this.deleteIndex, 1);
          })
          .catch((error) => {
            console.error('刪除預約時出錯:', error);
          });
      },
      // 取得資料
      fetchPatientDetails(patientId) {
      axios
        .post(api.domain + '/Patient/PatientInfo', { patientId })
        .then((response) => {
          console.log('Response data:', response.data);
          if (response.data && response.data.Data) {
            const patientData = response.data.Data;
            if (patientData.PatientID == patientId) {
              this.form = {
                ...this.form,
                ...patientData,
                Families: patientData.Families.map(family => ({
                  SeqNo: family.SeqNo || '',
                  FamilyName: family.FamilyName || '',
                  Relationship: family.Relationship || '',
                  PatientID: family.PatientID || '',
                  Tel: family.Tel || '',
                  PhoneNo: family.PhoneNo || '',                  
                  Company: family.Company || ''
                }))
              };
            } else {
              console.error('Patient not found in the response data');
            }
          } else {
            console.error('Unexpected response structure:', response);
          }
        })
        .catch((error) => {
          console.error('Error fetching patient details:', error);
        });
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
  
  .ButtonBack {
    margin-top: 20px;
    margin-left: 1%;
  }
  
  .buttons {
    display: flex;
    margin-left: 44%;
    
  }
  .el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  
  .el-form-item {
    margin-left: 0px; /* 調整表單欄位距左的空白 */
    margin-bottom: 15px;
    right: 70%; /* 調整表單的寬度位置 */
  }
}
@media (max-width: 800px){
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
  
  .ButtonBack {
    margin-top: 20px;
    margin-left: 1%;
  }
  
  .buttons {
    display: flex;
    margin-top: 15px;
    margin-left: 24%;
  }
  .el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  .el-form-item {
    margin-left: -45px; /* 調整表單欄位距左的空白 */
    margin-bottom: 15px;
    right: 70%; /* 調整表單的寬度位置 */
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
    margin-left: 60%;
  }
  .el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
  }

  
  @media (max-width: 1348px){
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
    margin-left: 58%;
  }
  .el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  }
}


</style>
  