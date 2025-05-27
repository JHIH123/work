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
              <el-form-item label="Lab ID:">
                <el-input v-model="form.LabID" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Test type:">
                <el-input v-model="form.TestType" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Date of the Analysis:">
                <el-input v-model="form.DateOfTheAnalysis" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Pathologist:">
                <el-input v-model="form.Pathologist" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Patient ID:">
                <el-input v-model="form.PatientID" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Physician:">
                <el-input v-model="form.Physician" />
              </el-form-item>
            </el-col>
            <el-col :span="11">
              <el-form-item label="Date Requestd:">
                <el-input v-model="form.DateRequestd"></el-input>
              </el-form-item>
            </el-col>


            <el-col :span="22">
              <el-form-item label="Results:" >
                <el-input v-model="form.Results" type="textarea"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="22">
              <el-form-item label="Diagnosis:">
                <el-input v-model="form.Diagnosis" type="textarea"></el-input>
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
    name: 'NewFamily',
    components: {
      Back,
      DocumentChecked,
      Delete,
      DeleteConfirmation
    },
    data() {
      return {
        form: {
          SeqNo: 0,
          FamilyName: '',
          PatientID: '',
          Nationality: '',
          Relationship: '',
          Tel: '',
          PhoneNo: '',
          Company: '',
          Address: '',
          Note: ''
        },
      };
    },
    created() {
      const SeqNo = this.$route.query.seqNo; 
      if (SeqNo) {
        this.fetchFamily(SeqNo);
      }
    },
    methods: {
      // 顯示確認是否要返回的視窗
      showConfirmationDialog() {
        this.$refs.deleteConfirmation.showBackConfirmationModal();
      },
      //取資料
      fetchFamily(SeqNo) {
        axios
          .post(api.domain + '/Family/FamilyInfo', { SeqNo })
          .then((response) => {
            console.log('Response data:', response.data);
            if (response.data && response.data.Data) {
              const FamilyData = response.data.Data;
              if (FamilyData.SeqNo == SeqNo) {
                this.form = { ...this.form, ...FamilyData }; 
                console.log("Updated form data:", this.form);
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
      //新增
      handleSubmit() {
        const url = api.domain + '/Family/EditFamily';
        axios
          .post(url, this.form)
          .then((response) => {
            Swal.fire('Success', 'Data saved successfully', 'success')
              .then(() => {
                this.$router.back();
              });
            console.log('Save response:', response);
          })
          .catch((error) => {
            Swal.fire('Error', 'Failed to save data', 'error');
            console.error('Error saving data:', error);
          });
      },
      showDeleteModal() {
        this.$refs.deleteConfirmation.showDeleteModal();
      },
      //刪除
      handleDelete() {
        const apiUrl = api.domain + '/Family/DeleteFamily';
        axios
          .post(apiUrl, { SeqNo: this.form.SeqNo })
          .then((response) => {
            Swal.fire({
              title: 'The record has been deleted.',
              icon: 'success',
              confirmButtonText: 'Close'
            }).then(() => {
              this.$router.back();
            });
          })
          .catch((error) => {
            Swal.fire({
              title: 'Error deleting the record.',
              icon: 'error',
              confirmButtonText: 'Close'
            });
            console.error('Error deleting family record:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
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
  
  </style>
  