<template>
  <div class="card">
    <div class="header">
      <el-button type="primary" class="Looksbtn" @click="LookAppointments">
        Appointments
      </el-button>
      <el-button type="primary" class="Looksbtn" @click="LookPatients">
        Patient
      </el-button>
      <el-button type="primary" class="Looksbtn" @click="LookPrescription">
        Prescription
      </el-button>
    </div>
    
    <div class="LooksBlock">
      <!-- Appointments Table -->
      <b v-if="activeTab === 'appointments'" class="section-title">Recent Appointment:</b>
      <el-table v-if="activeTab === 'appointments'" :data="[Appts]" class="custom-table" style="width: 100%" @sort-change="handleSortChange">
        <el-table-column prop="AppointmentID" label="Appointment ID" width="170px" sortable="custom"></el-table-column>
        <el-table-column prop="PatientID" label="Patient ID" width="130px" sortable="custom"></el-table-column>
        <el-table-column prop="PatientName" label="Patient Name" width="140px" sortable="custom"></el-table-column>
        <el-table-column prop="UrgencyLevel" label="Urgency Level" width="150px" sortable="custom"></el-table-column>
        <el-table-column prop="AppointmentDate" label="Appointment Date" width="180px" sortable="custom"></el-table-column>
        <el-table-column prop="Specialty" label="Specialty" width="130px" sortable="custom"></el-table-column>
        <el-table-column prop="Doctor" label="Doctor" width="130px" sortable="custom"></el-table-column>
      </el-table>
      
      <!-- Patients Table -->
      <b v-if="activeTab === 'patients'" class="section-title">Patient Information:</b>
      <el-table v-if="activeTab === 'patients'" :data="[Pts]" class="custom-table" style="width: 100%" @sort-change="handleSortChange">
        <el-form-item label="Patient Information:" label-width="140px"></el-form-item>
        <el-table-column prop="PatientID" label="Patient ID" width="140px" sortable="custom"></el-table-column>
        <el-table-column prop="PatientName" label="Patient Name" width="160px" sortable="custom"></el-table-column>
        <el-table-column prop="Sex" label="Sex" width="120px" sortable="custom"></el-table-column>
        <el-table-column prop="Age" label="Age" width="120px" sortable="custom"></el-table-column>
        <el-table-column prop="Birthday" label="Date of Birth" width="180px" sortable="custom"></el-table-column>
        <el-table-column prop="HospitalStatus" label="Hospitation Status" width="180px" sortable="custom"></el-table-column>
        <el-table-column prop="PrimaryCare" label="Primary Care Doctor" width="200px" sortable="custom"></el-table-column>
      </el-table>
      
      <!-- Families Table -->
      <b v-if="activeTab === 'patients'" class="section-title">Families Information:</b>
      <el-table v-if="activeTab === 'patients'" :data="Pts.Families" class="custom-table" style="width: 100%" @sort-change="handleSortChange">
        <el-table-column prop="FamilyName" label="Name" width="150px" sortable="custom"></el-table-column>
        <el-table-column prop="Relationship" label="Relationship" width="150px" sortable="custom"></el-table-column>
        <el-table-column prop="PhoneNo" label="Phone No" width="150px" sortable="custom"></el-table-column>
        <el-table-column prop="Tel" label="TEL" width="150px" sortable="custom"></el-table-column>
        <el-table-column prop="Company" label="Company" width="150px" sortable="custom"></el-table-column>
      </el-table>
      
      <!-- Prescriptions Table -->
      <b v-if="activeTab === 'prescriptions'" class="section-title">Recent Prescription:</b>
      <el-table v-if="activeTab === 'prescriptions'" :data="RecentRx" class="custom-table prescriptions-table" style="width: 100%" @sort-change="handleSortChange">
        <el-table-column prop="TreatmentStart" label="Start of Treatment" width="180px" sortable="custom"></el-table-column>
        <el-table-column prop="TreatmentEnd" label="End of Treatment" width="180px" sortable="custom"></el-table-column>
        <el-table-column prop="IsPrint" label="Print" width="100px" sortable="custom"></el-table-column>
        <el-table-column prop="MedicamentID" label="Medicament" width="130px" sortable="custom"></el-table-column>
        <el-table-column prop="LotNo" label="Lot No." width="100px" sortable="custom"></el-table-column>
        <el-table-column prop="Indication" label="Indication" width="130px" sortable="custom"></el-table-column>
        <el-table-column prop="Dose" label="Dose" width="100px" sortable="custom"></el-table-column>
        <el-table-column prop="DoseUnit" label="Dose Unit" width="120px" sortable="custom"></el-table-column>
        <el-table-column prop="Form" label="Form" width="100px" sortable="custom"></el-table-column>
        <el-table-column prop="CommonDosage" label="Common Dosage" width="170px" sortable="custom"></el-table-column>
        <el-table-column prop="Qty" label="Quantity" width="130px" sortable="custom"></el-table-column>
        <el-table-column prop="CreateDate" label="Create Date" width="180px" sortable="custom"></el-table-column>
      </el-table>
    </div>

    <div class="EditBlock">
      <el-button @click="showConfirmationDialog" class="back-button">
        <el-icon><Back /></el-icon> Back
      </el-button>
      <el-row class="info-row">
        <el-form-item label="Appointment ID:" label-width="140px">
          <span>{{ Appts.AppointmentID }}</span>
        </el-form-item>
        <el-form-item label="Patient ID:" label-width="140px">
          <span>{{ Appts.PatientID }}</span>
        </el-form-item>
        <el-form-item label="Patient Name:" label-width="140px">
          <span>{{ Appts.PatientName }}</span>
        </el-form-item>
      </el-row>

      <!-- 輔助診斷欄位 -->
      <el-form :model="Dx" label-width="150px" class="form-block">
        <el-col :span="22">
          <el-form-item label="Chief Complaint:" label-width="130px">
            <el-input v-model="Dx.ChiefComplaint" type="textarea" placeholder="Please enter a Chief Complaint"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="22">
          <el-row type="flex" justify="space-between">
            <el-col :span="18">
              <el-form-item label="Auxiliary Diagnostic Information:" label-width="226px"></el-form-item>
            </el-col>
            <el-col :span="6" class="btn-right" label-height>
              <el-button type="primary" class="generate-button" @click="GenerateDiagnostics(Dx.ChiefComplaint)">Generate Auxiliary Diagnostic</el-button>
            </el-col>
          </el-row>
          <el-col :span="23" :offset="1">
            <el-input v-model="Dx.AuxDiagnosis" :rows="5" type="textarea" placeholder="Please Generate a Auxiliary Diagnostic" class="diagnosis-input"></el-input>
          </el-col>
        </el-col>
        
        <el-col :span="22">
          <el-row type="flex" justify="space-between">
            <el-col :span="18">
              <el-form-item label="Prescription:" label-width="100px"></el-form-item>
            </el-col>
            <el-col :span="6" class="btn-right">
              <el-button type="primary" class="new-medication-button" @click="NewMedication">New Medication</el-button>
            </el-col>
            <el-col :span="23" :offset="1">
              <el-table :data="Dx.Prescription" class="Dx.Prescription-table" style="width: 100%" @sort-change="handleSortChange">
                <el-table-column prop="TreatmentStart" label="Start of Treatment" width="180px" sortable="custom"></el-table-column>
                <el-table-column prop="TreatmentEnd" label="End of Treatment" width="180px" sortable="custom"></el-table-column>
                <el-table-column prop="IsPrint" label="Print" width="100px" sortable="custom"></el-table-column>
                <el-table-column prop="MedicamentID" label="Medicament" width="130px" sortable="custom"></el-table-column>
                <el-table-column prop="LotNo" label="Lot No." width="100px" sortable="custom"></el-table-column>
                <el-table-column prop="Indication" label="Indication" width="130px" sortable="custom"></el-table-column>
                <el-table-column prop="Dose" label="Dose" width="100px" sortable="custom"></el-table-column>
                <el-table-column prop="DoseUnit" label="Dose Unit" width="120px" sortable="custom"></el-table-column>
                <el-table-column prop="Form" label="Form" width="100px" sortable="custom"></el-table-column>
                <el-table-column prop="CommonDosage" label="Common Dosage" width="170px" sortable="custom"></el-table-column>
                <el-table-column prop="Qty" label="Quantity" width="130px" sortable="custom"></el-table-column>
                <el-table-column prop="CreateDate" label="Create Date" width="180px" sortable="custom"></el-table-column>
                <el-table-column label="Operations" width="160px">
                  <template #default="scope">
                    <el-icon @click="GetPrescription(scope.row.AppointmentID, scope.row.MedicamentID)" size="small">
                      <Edit />
                    </el-icon>
                    <el-icon @click="confirmDelete(scope.row.AppointmentID, scope.row.MedicamentID)" size="small">
                      <Delete />
                    </el-icon>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>
        </el-col>
        <!-- Prescription line視窗 -->
        <el-dialog
          title="Prescription line"
          v-model="showNewMedication"
          width="65%"
          @close="closeNewMedication">
          
          <!-- 欄位 -->
          <el-form :model="currentPrescription" label-width="120px" class="custom-form">
            <el-row>
              <el-col :span="10">
                <el-form-item label="Medicament:">
                  <el-input v-model="currentPrescription.MedicamentID"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Indication:">
                  <el-input v-model="currentPrescription.Indication"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Allow Substitution:" label-width="140px">
                  <el-checkbox v-model="currentPrescription.AllowSubsitution" />
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Print:">
                  <el-checkbox v-model="currentPrescription.IsPrint" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Form:">
                  <el-input v-model="currentPrescription.Form"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Administration Route:" label-width="150px">
                  <el-input v-model="currentPrescription.AdministrationRoute"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Start of Treatment:" label-width="140px">
                  <el-date-picker v-model="currentPrescription.TreatmentStart" type="datetime" />
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="End of Treatment:" label-width="140px">
                  <el-date-picker v-model="currentPrescription.TreatmentEnd" type="datetime" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Lot No.:">
                  <el-input v-model="currentPrescription.LotNo"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Create Date:">
                  <el-input v-model="currentPrescription.CreateDate" :disabled="true"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            
            <hr class="divider" />

            <!-- DOSAGE欄位 -->
            <b>DOSAGE</b>
            <el-row>
              <el-col :span="8" :pull="1">
                <el-form-item label="Dose:">
                  <el-input v-model="currentPrescription.Dose"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8" :pull="1">
                <el-form-item label="Dose Unit:">
                  <el-input v-model="currentPrescription.DoseUnit"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8" :pull="1">
                <el-form-item label="X:">
                  <el-input v-model="currentPrescription.Qty"></el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <hr class="divider" />

            <!-- COMMON DOSAGE欄位 -->
            <b>COMMON DOSAGE</b>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Common Dosage:" label-width="140px">
                  <el-input v-model="currentPrescription.CommonDosage" :disabled="true"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Admin hours:">
                  <el-input v-model="currentPrescription.AdminHours" :disabled="true"></el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <hr class="divider" />

            <!-- SPECIFIC DOSAGE欄位 -->
            <b>SPECIFIC DOSAGE</b>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Frequency:">
                  <el-input v-model="currentPrescription.Sp_Frequency"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Unit:">
                  <el-input v-model="currentPrescription.Sp_Unit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Treatment Duration:" label-width="140px">
                  <el-input v-model="currentPrescription.Sp_TreatmentDur"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Treatment Period:" label-width="140px">
                  <el-input v-model="currentPrescription.Sp_TreatmentPer"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Review:">
                  <el-date-picker v-model="currentPrescription.Sp_Review" type="datetime" />
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Quantity:">
                  <el-input v-model="currentPrescription.Sp_Qty"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="10">
                <el-form-item label="Refills:">
                  <el-input v-model="currentPrescription.Sp_Refills"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Comment:">
                  <el-input v-model="currentPrescription.Sp_Comment"></el-input>
                </el-form-item>
              </el-col>
            </el-row>

          </el-form>
          
          <!-- 跳窗底部的按钮 -->
          <span slot="footer" class="dialog-footer">
            <el-button @click="closeNewMedication">Cancel</el-button>
            <el-button type="primary" @click="saveNewMedication">Save</el-button>
          </span>
        </el-dialog>

        <!--最終診斷欄位-->
        <el-col :span="22">
          <el-row type="flex" justify="space-between">
            <el-col :span="18">
              <el-form-item label="Final Diagnosis:" label-width="120px"></el-form-item>
            </el-col>
            
            <el-col :span="6" class="btn-right">
              <el-button type="primary" class="copy-button" @click="copyDiagnosis">Copy Auxiliary Diagnostic</el-button>
            </el-col>
          </el-row>
          <el-col :span="23" :offset="1">
            <el-input v-model="Dx.FinalDiagnosis" :rows="5" type="textarea" placeholder="Please enter a Final Diagnosis" class="diagnosis-input"></el-input>
          </el-col>
        </el-col>

        <!--醫囑欄位-->
        <el-col :span="22">
          <el-row type="flex" justify="space-between">
            <el-col :span="18">
              <el-form-item label="Order:" label-width="60px"></el-form-item>
            </el-col>

            <el-col :span="6" class="btn-right">
              <el-button type="primary" class="generate-button" @click="GenerateOrder(Dx.ChiefComplaint,Dx.FinalDiagnosis)">Generate Order</el-button>
            </el-col>
          </el-row>

          <el-col :span="23" :offset="1">
            <el-input v-model="Dx.Orders" :rows="5" type="textarea" placeholder="Please enter a Doctor's Order" class="order-input"></el-input>
          </el-col>
        </el-col>

        <!-- 通用 Loading 動畫彈窗 -->
        <el-dialog v-model="loadingDialogVisible" width="30%" :modal="true" :close-on-click-modal="false" :show-close="false">
          <div class="dialog-content" v-loading="loading" element-loading-text="Generating, please wait...">
          </div>
        </el-dialog>

        <!-- 衛教資訊範圍 -->
        <el-col :span="21" class="health-education-block">
          <el-row type="flex" justify="space-between">
            <el-col :span="18" :pull="1">
              <el-form-item label="Health Education" label-width="135px" class="health-education-label"></el-form-item>
            </el-col>
            <el-col :span="4" class="btn-right">
              <!-- 生成衛教資訊按鈕 -->
              <el-button v-if="Dx.HealthEducation === ''" type="primary" class="generate-button" @click="GenerateHE(Dx.ChiefComplaint,Dx.FinalDiagnosis)">Generate Health Education</el-button>

              <!-- 當衛教資訊生成後，顯示圖標 -->
              <el-col :pull="1" class="VDD">
                <template v-if="Dx.HealthEducation != ''">
                  <el-icon @click="showHealthEducationDialog = true" size="20">
                    <View />
                  </el-icon>
                  <el-icon @click="DownloadHE" size="20">
                    <Download />
                  </el-icon>
                  <el-icon @click="showDeleteModalHE" size="20">
                    <Delete />
                  </el-icon>
                </template>
              </el-col>
            </el-col>
          </el-row>
        </el-col>

        <!-- 衛教資訊跳窗 -->
        <el-dialog
          title="Health Education"
          v-model="showHealthEducationDialog"
          width="50%"
          @close="closeHealthEducationDialog"
          v-if="showHealthEducationDialog"
        >
        
          <!-- el-table 中加入圖片與文字 -->
          <el-table :data="[Dx]" class="Dx.HealthEducation-table" style="width: 900px;">
            <el-table-column prop="HealthEducation" show-overflow-tooltip>
              <template v-slot="scope">
                <div class="image-container">
                  <!-- 使用 el-image 顯示圖片 -->
                  <img src="@/assets/template.png" class="responsive-image" @load="onImageLoad"/>
                  <!--<el-image
                    src="./assets/template.png"
                    fit="contain"
                    class="responsive-image"
                    @load="onImageLoad"
                  ></el-image>-->

                  <!-- 顯示文字，絕對定位到圖片上 -->
                  <div class="custom-text-Title">
                    {{ healthEducationTitle }}
                  </div>
                  <div class="custom-text-Content">
                    {{ healthEducationContent }}
                  </div>
                </div>
              </template>
            </el-table-column>
          </el-table>

          <span slot="footer" class="dialog-footer">
            <el-button class="GoDLHE" @click="DownloadHE">
              <el-icon>
                <Download />
              </el-icon>
              download
            </el-button>
          </span>
        </el-dialog>

      </el-form>

      <!--底部看診用按鈕-->
      <el-form-item class="action-buttons">
        <el-button type="primary" @click="DiagnosisSave">
          <el-icon><DocumentChecked /></el-icon> Save
        </el-button>
        <el-button type="danger" @click="DeleteAll">
          <el-icon><Delete /></el-icon> Delete
        </el-button>
      </el-form-item>

    </div>
  </div>
</template>

<script>
  import { Back, DocumentChecked, Delete,Loading } from '@element-plus/icons-vue';
  import DeleteConfirmation from '../components/DeleteConfirmation.vue';
  import * as api from '../api/api.js';
  import Swal from 'sweetalert2';
  import { ElDialog, ElIcon } from 'element-plus'; // 確認dialog和icon的引入
  import axios from 'axios';
  import html2canvas from 'html2canvas';
  import jsPDF from 'jspdf';
  
  export default {
    name: 'NewDiagnosis',
    components: {
      Back,
      DocumentChecked,
      Delete,
      DeleteConfirmation,
      Loading
    },
    data() {
      return {
        loadingDialogVisible: false, // 控制彈窗顯示與否
        loading: false, // 控制 loading 動畫
        showHealthEducationDialog: false, // 控制弹窗的变量
        showNewMedication: false, // 預設藥物填寫視窗
        activeTab: 'appointments', // 預設顯示的表格
        // Appointments資料
        Appts: {
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
        // Patients資料
        Pts: {
          "PatientID": '',
          "PatientName": '',
          "IDNumber": '',
          "Sex": '',
          "Birthday": '',
          "Age": '',
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
        // 近期Prescription資料
        RecentRx:[],
        // 暫存目前編輯的Prescription資料
        currentPrescription: {
          "EditType": '',
          "AppointmentID": '',
          "MedicamentID": '',
          "Indication": '',
          "AllowSubsitution": '',
          "IsPrint": '',
          "Form": '',
          "AdminRoute": '',
          "TreatmentStart": '',
          "TreatmentEnd": '',
          "LotNo": '',
          "Dose": '',
          "DoseUnit": '',
          "Qty": '',
          "CommonDosage": '',
          "AdminHours": '',
          "Sp_Frequency": '',
          "Sp_Unit": '',
          "Sp_TreatmentStart": '',
          "Sp_TreatmentEnd": '',
          "Sp_TreatmentDur": '',
          "Sp_TreatmentPer": '',
          "Sp_Review": '',
          "Sp_Qty": '',
          "Sp_Refills": '',
          "Sp_Comment": '',
          "CreateDate": ''
        },
        //Diagnosis資料
        Dx: {
          "ChiefComplaint": '',
          "AuxDiagnosis": '',
          "Prescription": [], // 用于存储所有的药物数据
          "FinalDiagnosis": '',
          "Orders": '',
          "HealthEducation": ''
        },
        appointmentsData:[],
        patientsData:[],
        prescriptionsData:[],
        GAIData:'',
        capturedImageData: null,
        healthEducationTitle: '',
        healthEducationContent: '',
      };
    },
    created() {
      const appointmentId = this.$route.query.appointmentid;
      if (appointmentId) {
        this.fetchAppointmentDetails(appointmentId);
        this.GetDiagnosis(appointmentId);
      }
    },
    methods: {
      closeHealthEducationDialog() {
        this.showHealthEducationDialog = false;
      },
      
      // 刪除視窗
      showDeleteModal(onConfirm) {
        Swal.fire({
          title: 'Do you really want to delete these records?',
          text: 'This process cannot be undone.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          cancelButtonText: 'Cancel',
          confirmButtonText: 'Delete',
        }).then((result) => {
          if (result.isConfirmed) {
            if (typeof onConfirm === 'function') {
              onConfirm(); // 調用回調函數
            } else {
              console.error('onConfirm is not a function');
            }
            Swal.fire({
              title: 'The record has been deleted.',
              icon: 'success',
              confirmButtonText: 'Close',
            })
          }
        });
      },
      //返回通知視窗
      showBackConfirmationModal() {
        Swal.fire({
          title: 'Are you sure?',
          text: 'Upon exit, records will not be saved.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          cancelButtonText: 'Cancel',
          confirmButtonText: "Yes, I'm sure"
        }).then((result) => {
          if (result.isConfirmed) {
            // 向父組件傳遞返回確認事件
            this.$router.back();
          }
        });
      },
      // Health Education刪除視窗
      showDeleteModalHE() {
        Swal.fire({
          title: 'Do you really want to delete these records?',
          text: 'This process cannot be undone.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          cancelButtonText: 'Cancel',
          confirmButtonText: 'Delete',
        }).then((result) => {
          if (result.isConfirmed) {
            // 清空 HealthEducation
            this.Dx.HealthEducation = ''; 

            Swal.fire({
              title: 'The record has been deleted.',
              icon: 'success',
              confirmButtonText: 'Close',
            });
          }
        });
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
      LookAppointments() {
        this.activeTab = 'appointments';
      },
      LookPatients() {
        this.activeTab = 'patients';
      },
      LookPrescription() {
        this.activeTab = 'prescriptions';
      },
      // 取得 Appointments 資料
      fetchAppointmentDetails(appointmentId) {
        axios
          .post(api.domain + '/Appointment/AppointmentInfo', { appointmentId })
          .then((response) => {
            if (response.data && response.data.Data) {
              // 確保 API 回應結構與你的程式碼一致
              this.appointmentsData = [response.data.Data]; // 如果資料不是陣列，需要將其包裝成陣列
              
              // 更新表單數據以確保反應性
              if (this.appointmentsData[0].AppointmentID === appointmentId) {
                Object.assign(this.Appts, this.appointmentsData[0]);
                this.fetchPatientDetails(this.Appts.PatientID)
                this.fetchThistRx(this.Appts.AppointmentID)
                this.fetchRecentRx(this.Appts.PatientID, this.Appts.AppointmentID)
              }
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching appointment details:', error);
          });
      },
      // 取得 Patients 資料
      fetchPatientDetails(patientId) {
        axios
          .post(api.domain + '/Patient/PatientInfo', { patientId })
          .then((response) => {
            if (response.data && response.data.Data) {
              // 確保 API 回應結構與你的程式碼一致
              this.patientsData = [response.data.Data];
              
              // 更新 Pts 物件
              if (this.patientsData[0].PatientID === patientId) {
                // 使用 Object.assign 更新 Pts 物件，以確保響應性
                Object.assign(this.Pts, this.patientsData[0]);
              }
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          });
      },
      // 取得近期 Prescription 列表
      fetchRecentRx(patientId, appointmentId) {
        axios
          .post(api.domain + '/Prescription/PrescriptionList', 
            { ViewMode: 'Normal', PatientID: patientId })  // 'Normal' 需要加上引號
          .then((response) => {
            if (response.data && response.data.Data) {
              // 儲存原始資料
              this.prescriptionsData = response.data.Data;
              // 過濾掉 AppointmentID 等於指定值的資料
              this.RecentRx = this.prescriptionsData.filter(item => item.AppointmentID !== appointmentId);
              // 列印出過濾後的資料
              console.log('Filtered RecentRx:', this.RecentRx);
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          });
      },
      // 取得此筆 Prescription 列表
      fetchThistRx(appointmentId) {
        axios
          .post(api.domain + '/Prescription/PrescriptionList', 
            { ViewMode: 'Normal', AppointmentID: appointmentId })
          .then((response) => {
            if (response.data && response.data.Data) {              
              // 確保 API 回應結構與你的程式碼一致
              this.prescriptionsData = response.data.Data;
              
              // 檢查所有的 AppointmentID 是否都等於指定的 appointmentId
              const allMatch = this.prescriptionsData.every(item => item.AppointmentID === appointmentId);

              if (allMatch) {
                this.Dx.Prescription = this.prescriptionsData;
                // 列印出過濾後的資料
                console.log('Filtered ThistRx:', this.Dx.Prescription);
              }
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          });
      },
      // 取得完整 Prescription 資料
      GetPrescription(appointmentId,medicamentId) {
        axios
          .post(api.domain + '/Prescription/PrescriptionInfo', 
            { AppointmentID: appointmentId, MedicamentID: medicamentId })
          .then((response) => {
            if (response.data && response.data.Data) {
              // 確保 API 回應結構與你的程式碼一致
              this.prescriptionsInfoData = response.data.Data;

              // 更新表單數據以確保反應性
              if (this.prescriptionsInfoData.AppointmentID === appointmentId) {
                //更改this.currentPrescription的EditType為Edit
                this.currentPrescription = {
                  "EditType": 'Edit',
                  "AppointmentID": '',
                  "MedicamentID": '',
                  "Indication": '',
                  "AllowSubsitution": '',
                  "IsPrint": '',
                  "Form": '',
                  "AdminRoute": '',
                  "TreatmentStart": '',
                  "TreatmentEnd": '',
                  "LotNo": '',
                  "Dose": '',
                  "DoseUnit": '',
                  "Qty": '',
                  "CommonDosage": '',
                  "AdminHours": '',
                  "Sp_Frequency": '',
                  "Sp_Unit": '',
                  "Sp_TreatmentStart": '',
                  "Sp_TreatmentEnd": '',
                  "Sp_TreatmentDur": '',
                  "Sp_TreatmentPer": '',
                  "Sp_Review": '',
                  "Sp_Qty": '',
                  "Sp_Refills": '',
                  "Sp_Comment": '',
                  "CreateDate": ''
                }
                Object.assign(this.currentPrescription, this.prescriptionsInfoData);
                // 切割 Sp_TreatmentPer 並分別賦值給 Sp_TreatmentStart 和 Sp_TreatmentEnd
                if (this.currentPrescription.Sp_TreatmentPer) {
                  const treatmentPeriod = this.currentPrescription.Sp_TreatmentPer.split(' ~ ');
                  this.currentPrescription.Sp_TreatmentStart = treatmentPeriod[0];
                  this.currentPrescription.Sp_TreatmentEnd = treatmentPeriod[1];
                }
                console.log('test5',this.currentPrescription)
                this.showNewMedication = true;
              }
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          });
      },
      // 編輯&儲存 Prescription 資料
      EditPrescription(){
        //console.log('查看日期1',this.currentPrescription.TreatmentStart);

        // 轉換現有的是可行的
        // 將 TreatmentStart、TreatmentEnd 轉換為目標格式
        const treatmentStart = new Date(this.currentPrescription.TreatmentStart);
        this.currentPrescription.TreatmentStart = this.formatDateTime(treatmentStart);
        //console.log('查看日期2',this.currentPrescription.TreatmentStart);
        
        const treatmentEnd = new Date(this.currentPrescription.TreatmentEnd);
        this.currentPrescription.TreatmentEnd = this.formatDateTime(treatmentEnd);

        // 切割 Sp_TreatmentPer 並分別賦值給 Sp_TreatmentStart 和 Sp_TreatmentEnd
        if (this.currentPrescription.Sp_TreatmentPer) {
          const treatmentPeriod = this.currentPrescription.Sp_TreatmentPer.split(' ~ ');
          this.currentPrescription.Sp_TreatmentStart = treatmentPeriod[0];
          this.currentPrescription.Sp_TreatmentEnd = treatmentPeriod[1];
        }
        // 將 Sp_TreatmentStart、Sp_TreatmentEnd 和 Sp_Review 也進行格式轉換
        const spTreatmentStart = new Date(this.currentPrescription.Sp_TreatmentStart);
        this.currentPrescription.Sp_TreatmentStart = this.formatDateTime(spTreatmentStart);

        const spTreatmentEnd = new Date(this.currentPrescription.Sp_TreatmentEnd);
        this.currentPrescription.Sp_TreatmentEnd = this.formatDateTime(spTreatmentEnd);

        const spReview = new Date(this.currentPrescription.Sp_Review);
        this.currentPrescription.Sp_Review = this.formatDateTime(spReview);

        // 將 AllowSubsitution、IsPrint 轉換為 'Y' 或 'N'
        this.currentPrescription.AllowSubsitution = this.currentPrescription.AllowSubsitution ? 'Y' : 'N';
        this.currentPrescription.IsPrint = this.currentPrescription.IsPrint ? 'Y' : 'N';

        //console.log('檢查傳送數值:',this.currentPrescription);

        axios
          .post(api.domain + '/Prescription/EditPrescription', this.currentPrescription)
          .then((response) => {
            this.closeNewMedication();
            Swal.fire({
              title: 'The record has been saved.',
              icon: 'success',
              confirmButtonText: 'Close'
            });
          })
          .catch((error) => {
            this.closeNewMedication();
            Swal.fire({
              title: 'Error saving the record.',
              icon: 'error',
              confirmButtonText: 'Close'
            });
            console.error('Error saving patient:', error);
          });
      },
      // 刪除視窗使用
      confirmDelete(appointmentId, medicamentId) {
        this.deleteappointmentId = appointmentId;
        this.deletemedicamentId = medicamentId;
        this.showDeleteModal(() => this.DeletePrescription());
      },
      // 刪除 Prescription 資料
      DeletePrescription() {
        axios
          .post(api.domain + '/Prescription/DeletePrescription', {
            AppointmentID: this.deleteappointmentId, MedicamentID: this.deletemedicamentId})
          .then((response) => {
            console.log('刪除回應:', response.data);
            // 更新列表資料，使用 取得此筆處方簽資料()
            this.fetchThistRx(this.deleteappointmentId);
          })
          .catch((error) => {
            console.error('刪除預約時出錯:', error);
          });
      },
      // 顯示確認是否要返回的視窗
      showConfirmationDialog() {
        this.showBackConfirmationModal();
      },
      // Generate Auxiliary Diagnostic 按鈕
      GenerateDiagnostics(ChiefComplaint) {
        if(ChiefComplaint){

          // 顯示 loading 視窗
          this.loadingDialogVisible = true;
          this.loading = true;

          axios
          .post('http://127.0.0.1:8000/AuxiliaryDiag', { diagnosisInfo: ChiefComplaint })
          .then((response) => {
            if (response.data) {
              // 提取 content 屬性中的字串資料
              this.GAIData = response.data.content;
              console.log("查看1:",this.GAIData);
              console.log("查看2:",response.data);
              // 呼叫格式化方法
              this.formatContentDx();
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          })
          .finally(() => {
            // 無論請求成功或失敗，關閉 loading 視窗
            this.loadingDialogVisible = false;
            this.loading = false;
          });
        }
        else{
          console.log('Chief Complaint 是空的，請檢察');
        }
      },
      // Order 按鈕
      GenerateOrder(ChiefComplaint,FinalDiagnosis){
        if(ChiefComplaint && FinalDiagnosis){

          // 顯示彈窗和 loading
          this.loadingDialogVisible = true;
          this.loading = true;

          // 將 FinalDiagnosis 轉換成單行字串並移除換行符號，保持診斷之間有數字和冒號分隔
          const formattedFinalDiagnosis = FinalDiagnosis
            .replace(/\n/g, '')  // 移除換行符號
            .replace(/(\d+\.)/g, '$1 ')  // 確保數字後有空格
            .trim();  // 去除首尾多餘的空格
          
          // 格式化 diagnosisInfo 並保持單行格式發送至 API
          const DiagnosisInfo = `主訴: ${ChiefComplaint}, 最終診斷: ${formattedFinalDiagnosis}`;
          
          // 在發送 API 前檢查字串格式
          console.log("Order API檢查： "+DiagnosisInfo);

          axios
          .post('http://127.0.0.1:8000/AuxiliaryOrder', { diagnosisInfo: DiagnosisInfo })
          .then((response) => {
            if (response.data) {
              // 提取 content 屬性中的字串資料
              this.GAIData = response.data.content;
              console.log("查看1:",this.GAIData);
              console.log("查看2:",response.data);
              // 呼叫格式化方法
              this.formatContentORD();
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          })
          .finally(() => {
            // 無論請求成功或失敗，關閉 loading 視窗
            this.loadingDialogVisible = false;
            this.loading = false;
          });
        }
        else{
          console.log('Chief Complaintc 或 FinalDiagnosis 是空的，請檢察');
        }
      },
      // Health Education 按鈕
      GenerateHE(ChiefComplaint, FinalDiagnosis) {
        if (ChiefComplaint && FinalDiagnosis) {
          // 顯示彈窗和 loading
          this.loadingDialogVisible = true;
          this.loading = true;

          // 將 FinalDiagnosis 轉換成單行字串並移除換行符號，保持診斷之間有數字和冒號分隔
          const formattedFinalDiagnosis = FinalDiagnosis
            .replace(/\n/g, '') // 移除換行符號
            .replace(/(\d+\.)/g, '$1 ') // 確保數字後有空格
            .trim(); // 去除首尾多餘的空格

          // 格式化 DiagnosisInfo 並保持單行格式發送至 API
          const DiagnosisInfo = `主訴: ${ChiefComplaint}, 最終診斷: ${formattedFinalDiagnosis}`;

          console.log("Health Education API檢查： " + DiagnosisInfo); // 在發送 API 前檢查字串格式

          axios
            .post('http://127.0.0.1:8000/HealthEducation', { diagnosisInfo: DiagnosisInfo })
            .then((response) => {

              if (response.data) {
                // 提取 content 屬性中的字串資料
                this.GAIData = response.data.content;
                console.log("查看1:", this.GAIData);
                console.log("查看2:", response.data);
                // 呼叫格式化方法
                this.formatContentHE();
              } else {
                console.error('Unexpected response structure:', response);
              }
            })
            .catch((error) => {

              console.error('Error fetching patient details:', error);
            })
            .finally(() => {
              this.loadingDialogVisible = false; // 關閉彈窗
              this.loading = false; // 停止 loading
            });
        } else {
          console.log('Chief Complaint 或 FinalDiagnosis 是空的，請檢查');
        }
      },
      // 格式化 Auxiliary Diagnostic Informatione 顯示資料
      formatContentDx() {
        this.Dx.AuxDiagnosis = this.GAIData
        .replace(/\*\*(.*?)\*\*/g, '$1')  // 移除 **粗體** 標記
        .replace(/###\s*/g, '')           // 移除 ### 標記及其後面的空白
        .replace(/\*(.*?)\*/g, '$1');     // 移除 *斜體* 標記
        this.GAIData = '';
      },
      // 格式化 Order 顯示資料
      formatContentORD() {
        this.Dx.Orders = this.GAIData
        .replace(/\*\*(.*?)\*\*/g, '$1')  // 移除 **粗體** 標記
        .replace(/###\s*/g, '')           // 移除 ### 標記及其後面的空白
        .replace(/\*(.*?)\*/g, '$1');     // 移除 *斜體* 標記
        this.GAIData = '';
      },
      // 格式化 Health Education 顯示資料
      formatContentHE() {
        this.Dx.HealthEducation = this.GAIData
        .replace(/####\s*/g, '')          // 移除 #### 標記及其後面的空白
        .replace(/\*\*(.*?)\*\*/g, '$1')  // 移除 **粗體** 標記
        .replace(/###\s*/g, '')           // 移除 ### 標記及其後面的空白
        .replace(/\*(.*?)\*/g, '$1');     // 移除 *斜體* 標記
        this.formatHealthEducation();
        this.GAIData = '';
        this.showHealthEducationDialog = true;
      },

      // 當圖片加載時捕捉圖片
      onImageLoad() {
        console.log('圖片加載完成');
        this.$nextTick(() => {
          this.capturePreviewContent(); // 確保圖片加載完成後觸發捕捉
        });
      },
      // 捕捉預覽內容並存儲為圖片數據
      capturePreviewContent() {
        console.log('正在捕捉');
        const element = document.querySelector('.image-container');

        if (!element) {
          console.error('找不到指定的 HTML 元素');
          return;
        }

        html2canvas(element, { scale: 2 }).then((canvas) => {
          this.capturedImageData = canvas.toDataURL('image/png');
          console.log('捕捉成功');
        }).catch((error) => {
          console.error('捕捉預覽內容失敗:', error);
        });
      },
      // 下載 Health Education 顯示資料
      DownloadHE(){
        if (!this.capturedImageData) {
          console.warn('沒有已捕捉的圖片數據，將重新捕捉圖片。');
          
          const element = document.querySelector('.image-container'); // 根據 DOM 結構選擇
          if (!element) {
            console.error('找不到指定的 HTML 元素');
            return;
          }

          // 使用 html2canvas 將 HTML 內容轉換為 Canvas
          html2canvas(element, { scale: 2 }).then((canvas) => {
            // 轉換為圖像數據
            const imgData = canvas.toDataURL('image/png');

            // 創建 jsPDF 文件
            const pdf = new jsPDF({
              orientation: 'portrait', // 根據需要設置
              unit: 'px',
              format: [canvas.width, canvas.height], // 設置 PDF 大小與 Canvas 一致
            });

            // 將圖像數據添加到 PDF
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);

            // 下載 PDF 文件
            pdf.save('HealthEducation.pdf');
          }).catch((error) => {
            console.error('PDF 生成失敗:', error);
          });
        } else {
          // 如果已有捕捉到的圖片數據，直接使用它生成 PDF
          const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'px',
            format: [500, 700], // 設置 PDF 大小
          });

          pdf.addImage(this.capturedImageData, 'PNG', 0, 0, 500, 700);
          pdf.save('HealthEducation.pdf');
        }
      },
      // New Medication 按鈕
      NewMedication() {
        this.currentPrescription = {
          "EditType": 'New',
          "AppointmentID": this.Appts.AppointmentID,
          "MedicamentID": '',
          "Indication": '',
          "AllowSubsitution": '',
          "IsPrint": '',
          "Form": '',
          "AdminRoute": '',
          "TreatmentStart": '',
          "TreatmentEnd": '',
          "LotNo": '',
          "Dose": '',
          "DoseUnit": '',
          "Qty": '',
          "CommonDosage": '',
          "AdminHours": '',
          "Sp_Frequency": '',
          "Sp_Unit": '',
          "Sp_TreatmentStart": '',
          "Sp_TreatmentEnd": '',
          "Sp_TreatmentDur": '',
          "Sp_TreatmentPer": '',
          "Sp_Review": '',
          "Sp_Qty": '',
          "Sp_Refills": '',
          "Sp_Comment": '',
          "CreateDate": ''
        };
        this.showNewMedication = true;
      },
      // Prescription line 關閉按鈕
      closeNewMedication() {
        this.showNewMedication = false;
      },
      // Prescription line 儲存按鈕
      async saveNewMedication() {
        try {
          // 先儲存新的處方簽資料
          await this.EditPrescription(); // 等待處方簽資料儲存完成

          // 取得更新後的處方簽資料並更新到 Dx.Prescription 中
          await this.fetchThistRx(this.Appts.AppointmentID);
        }
        catch (error) {
          console.error('Error in saveNewMedication:', error);
        }
      },
      // Copy Auxiliary Diagnostic 按鈕
      copyDiagnosis() {
        this.Dx.FinalDiagnosis = this.Dx.AuxDiagnosis;
      },
      //資料排序
      handleSortChange({ column, prop, order }) {
        console.log('Sort change:', column, prop, order);
        this.tableData.sort((a, b) => {
          if (order === 'ascending') {
            return a[prop] > b[prop] ? 1 : -1;
          } else {
            return a[prop] < b[prop] ? 1 : -1;
          }
        });
      },
      // Health Education 資訊前端格式化
      formatHealthEducation() {
        if (this.Dx.HealthEducation) {
          // 移除特定說明文字並處理開頭與結尾的多餘空行
          let formattedHealthEducation = this.Dx.HealthEducation
            .replace(/(衛教資訊摘要|衛教資訊內容|摘要標題)：?/g, '') // 移除特定說明文字
            .replace(/^\s*\n+/, '')                                   // 移除開頭的多餘換行和空格
            .replace(/\n\s*$/, '')                                    // 移除結尾的多餘換行和空格
            .replace(/\n{3,}/g, '\n');       // 將連續的多餘換行符號減少為最多2個換行

          const paragraphs = formattedHealthEducation.split('\n'); // 以換行分割段落
          this.healthEducationTitle = paragraphs[0] || '';         // 第一段作為標題
          this.healthEducationContent = paragraphs.slice(1).join('\n') || ''; // 其餘段落合併為內容
        
          console.log('查看HealthEducation標題:',this.healthEducationTitle);
          console.log('查看HealthEducation內文:',this.healthEducationContent);
        }
      },
      // 取得 Diagnosis 資訊
      GetDiagnosis(appointmentId){
        axios
          .post(api.domain + '/Diagnosis/DiagnosisInfo', { AppointmentID: appointmentId })
          .then((response) => {
            if (response.data && response.data.Data) {
              // 確保 API 回應結構與你的程式碼一致
              this.DxData = [response.data.Data]; // 如果資料不是陣列，需要將其包裝成陣列
              
              // 更新表單數據以確保反應性
              if (this.DxData[0].AppointmentID === appointmentId) {
                Object.assign(this.Dx, this.DxData[0]);
                console.log('查看HealthEducation:',this.Dx.HealthEducation);
                this.formatHealthEducation(); // 呼叫方法格式化 Health Education
              }
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching appointment details:', error);
          });
      },
      // 儲存 Diagnosis 資訊
      DiagnosisSave(){
        // 發送 API 請求
        axios
          .post(api.domain + '/Diagnosis/EditDiagnosis', { 
            AppointmentID: this.Appts.AppointmentID, 
            ChiefComplaint: this.Dx.ChiefComplaint,
            AuxDiagnosis: this.Dx.AuxDiagnosis,
            FinalDiagnosis: this.Dx.FinalDiagnosis,
            Orders: this.Dx.Orders,
            HealthEducation: this.Dx.HealthEducation
          })
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
            console.error('Error saving Diagnosis:', error);
          });
      },
      // Diagnosis 刪除詢問
      DeleteAll() {
        this.showDeleteModal(() => {
          this.DiagnosisDelete();
          this.DeleteAllPrescription();
        });
      },
      // 刪除 Diagnosis 資訊
      DiagnosisDelete() {
        axios
          .post(api.domain + '/Diagnosis/EditDiagnosis', { 
              AppointmentID: this.Appts.AppointmentID, 
              ChiefComplaint: '',
              AuxDiagnosis: '',
              FinalDiagnosis: '',
              Orders: '',
              HealthEducation: ''
            })
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
      // 刪除看診所有 Prescription 資料
      DeleteAllPrescription() {
        // 從 Dx.Prescription 中提取所有 MedicamentID
        const medicamentIds = this.Dx.Prescription.map(prescription => prescription.MedicamentID);

        // 針對每個 MedicamentID 發送單獨的 API 請求
        medicamentIds.forEach((medicamentId) => {
          axios
            .post(api.domain + '/Prescription/DeletePrescription', {
              AppointmentID: this.Appts.AppointmentID,  // 傳入 AppointmentID
              MedicamentID: medicamentId  // 傳入單個 MedicamentID
            })
            .then((response) => {
              console.log(`刪除處方 ${medicamentId} 成功:`, response.data);
              // 如果需要的話，可以在這裡做更多的操作，例如每次成功刪除後，更新本地的 Prescription 列表
            })
            .catch((error) => {
              console.error(`刪除處方 ${medicamentId} 時出錯:`, error);
            });
        });

        // 最後，清空本地 Dx.Prescription
        this.Dx.Prescription = [];
      },
    }
  };
</script>
  
<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Chocolate+Classical+Sans&display=swap');
  
  
  @media (max-width: 1024px){
    .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .header {
    display: flex;
  }
  .card {
    background-color: #eaf5fc;
    border-radius: 30px;
    padding: 15px;
    width: auto;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  }
  .LooksBlock {
    background-color: #F6FCF3; /* 背景顏色 */
    padding: 20px; /* 內邊距 */
    border-radius: 30px; /* 圓角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
    margin-bottom: 10px;
  }
  .EditBlock{
    background-color: #ffffff;
    border-radius: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
  }
  .form-block{
    padding: 10px;
  }
  /*上方查看列表CSS*/
  .section-title {
    display: block;
    margin-bottom: 10px; /* 與表格之間的間距 */
    margin-top: 20px; /* 與上方元素之間的間距 */
    font-weight: bold;
    font-size: 16px;
    color: #333;
  }
  .custom-table {
    background-color: #F6FCF3; /* 背景顏色 */
    border-radius: 10px; /* 圓角 */
  }
  .custom-table :deep(.el-table__header-wrapper),
  .custom-table :deep(.el-table__body-wrapper),
  .custom-table :deep(.el-table__header),
  .custom-table :deep(.el-table__body) {
    background-color: #F6FCF3; /* 背景顏色 */
  }
  .custom-table :deep(.el-table__header-wrapper th),
  .custom-table :deep(.el-table__body-wrapper td) {
    background-color: #F6FCF3; /* 背景顏色 */
    border-bottom: 1px solid #e0e0e0; /* 底部邊框 */
  }
  .Rx-table {
    border-radius: 6px; /* 圆角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
    margin-top: 10px; /* 与上方元素的间距 */
  }
  .el-form-item {
    margin-left: 50px;
    right: 70%;
    margin-bottom: 20px;
    margin-top: 10px;
  }
  .el-button {
    margin-top: 6px;
    margin-left: 1%;
    margin-bottom: 15px;
  }
  .action-buttons {
    margin-left: 65%;
  }
  .back-button{
    margin-top: 15px;
  }
  .dialog-footer{
    margin-left: 85%;
  }
  .custom-form .compact-form-item {
    margin-bottom: 12px; /* 仅对特定表单项之间的距离进行调整 */
  }
  .custom-form .form-input {
    height: 38px; /* 仅对特定表单项中的输入框进行高度调整 */
  }
  /* Prescription line 分割線*/ 
  .divider {
    border: none;
    border-top: 1px solid #ccc; /* 线条的颜色和宽度 */
    margin: 20px 0; /* 上下的间距 */
  }
  .Looksbtn {
    color: #777777;
    border: 1px solid #F6FCF3;
    height: 32px;
    border-radius: 16px;
    padding: 0 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    background-color: #F6FCF3;
    cursor: pointer;
    font-size: 14px;
    text-decoration: none;
  }
  .Looksbtn.active {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .Looksbtn:hover {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .info-row{
    padding: 10px;
  }
  /*欄位通用設定*/
  .btn-right {
    text-align: right;
    margin-top: 10px;
  }
  .btn-right .el-icon {
    margin-left: -6px;  /* 控制圖標之間的間距 */
    margin-right: 10px;
    margin-top: 10px;
  }
  .diagnosis-input {
    margin-top: 10px; /* 與標籤和按鈕的間距 */
    border-radius: 10px; /* 使輸入框具有圓角 */
    background-color: #eeeeee; /* 使輸入框的背景顏色與圖片中的類似 */
    width: 100%; /* 使輸入框填滿行寬 */
    box-sizing: border-box; /* 確保 padding 和 border 不會影響寬度計算 */
  }
  /*Auxiliary Diagnostic Information*/
  .generate-button {
    margin-left: -50px;
    background: linear-gradient(0.35turn,#B9C3F5, #DD73DF);
    color: #ffffff;
    border-color: #ffffff;
    border-radius: 16px;
  }
  .generate-button.active {
    background: linear-gradient(0.35turn,#7179a3, #7e3d80);
    color: #464343;
    border-color: #464343;
  }
  .generate-button:hover {
    
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: #c5c5c5;
    border-color: #8f8f8f;
  }
  /*Prescription*/
  .new-medication-button{
    
    background-color: #e0bcdd;
    color: #000000;
    border-color: #e0bcdd;
    border-radius: 16px;
  }
  .new-medication-button.active {
    background-color: #8a5f86;
    color: #50474f;
    border-color: #50474f;
  }
  .new-medication-button:hover {
    background-color: #aa79a6;
    color: #524350;
    border-color: #524350;
  }
  /*Final Diagnosis*/
  .copy-button {
    margin-left: -40px;
    background-color: #E8E7E0;
    color: #000000;
    border-color: #E8E7E0;
    border-radius: 16px;
  }
  .copy-button.active {
    background-color: #88867c;
    color: #757575;
    border-color: #757575;
  }
  .copy-button:hover {
    background-color: #bdbbb1;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }  
  .health-education-block {
    margin-left: 25px;
    margin-top: 20px;
    padding-right: 67px;
    background-color: pink;
    border-radius: 8px;
    width: auto; /* 保持自適應 */
  }
  /* 衛教圖片下載 */
  .GoDLHE {
    margin-left: -50px;
    background-color: #B098E2;
    color: #ffffff;
  }
  .GoDLHE.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .GoDLHE:hover {
    background-color: #947ec4;
    color: #dddddd;
  }
  .pink-button {
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: white; /* 按钮文字颜色 */
  }
  /* 圖片容器設定相對定位 */
  .image-container {
    position: relative;
    width: 100%; /* 根據需要調整寬度 */
    height: auto;
  }
  /* 圖片等比例縮放 */
  .responsive-image {
    width: 100%;
    height: auto;
  }
  /* 衛教標題文字 */
  .custom-text-Title {
    position: absolute;
    top: 40px; /* 根據需要調整文字的垂直位置 */
    left: 70px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 0px;
    white-space: pre-line;
    word-break: break-word;
    font-size: 20px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  /* 衛教內文文字 */
  .custom-text-Content {
    position: absolute;
    top: 100px; /* 根據需要調整文字的垂直位置 */
    left: 10px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 15px;
    white-space: pre-line; 
    word-break: break-word;
    font-size: 11px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  .pink-button:hover {
    background-color: #8f8f8f; /* 鼠标悬浮时的按钮颜色 */
  }
  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: contain; /* 圖片大小設置為等比例縮放 */
    background-repeat: no-repeat; /* 防止背景重複 */
  }
  }
  @media (max-width: 800px){
    
    .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .header {
    display: flex;
  }
  .card {
    background-color: #eaf5fc;
    border-radius: 30px;
    padding: 15px;
    width: auto;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  }
  .LooksBlock {
    background-color: #F6FCF3; /* 背景顏色 */
    padding: 20px; /* 內邊距 */
    border-radius: 30px; /* 圓角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
    margin-bottom: 10px;
  }
  .EditBlock{
    background-color: #ffffff;
    border-radius: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
  }
  .form-block{
    padding: 10px;
  }
  /*上方查看列表CSS*/
  .section-title {
    margin-bottom: 10px; /* 與表格之間的間距 */
    margin-top: 20px; /* 與上方元素之間的間距 */
    font-size: 16px;
    color: #333;
  }
  .custom-table {
    background-color: #F6FCF3; /* 背景顏色 */
    border-radius: 10px; /* 圓角 */
  }
  .custom-table :deep(.el-table__header-wrapper),
  .custom-table :deep(.el-table__body-wrapper),
  .custom-table :deep(.el-table__header),
  .custom-table :deep(.el-table__body) {
    background-color: #F6FCF3; /* 背景顏色 */
  }
  .custom-table :deep(.el-table__header-wrapper th),
  .custom-table :deep(.el-table__body-wrapper td) {
    background-color: #F6FCF3; /* 背景顏色 */
    border-bottom: 1px solid #e0e0e0; /* 底部邊框 */
  }
  .Rx-table {
    border-radius: 6px; /* 圆角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
    margin-top: 10px; /* 与上方元素的间距 */
  }
  .el-form-item {
    margin-left: 50px;
    right: 70%;
    margin-bottom: 20px;
    margin-top: 10px;
  }
  .el-button {
    margin-top: 6px;
    margin-left: 1%;
    margin-bottom: 15px;
  }
  .action-buttons {
    margin-left: 57%;
  }
  .back-button{
    margin-left: 15px;
    margin-top: 15px;
  }
  .dialog-footer{
    margin-left: 85%;
  }
  .custom-form .compact-form-item {
    margin-bottom: 12px; /* 仅对特定表单项之间的距离进行调整 */
  }
  .custom-form .form-input {
    height: 38px; /* 仅对特定表单项中的输入框进行高度调整 */
  }
  /* Prescription line 分割線*/ 
  .divider {
    border: none;
    border-top: 1px solid #ccc; /* 线条的颜色和宽度 */
    margin: 20px 0; /* 上下的间距 */
  }
  .Looksbtn {
    color: #777777;
    border: 1px solid #F6FCF3;
    height: 32px;
    border-radius: 16px;
    padding: 0 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    background-color: #F6FCF3;
    cursor: pointer;
    font-size: 14px;
    text-decoration: none;
  }
  .Looksbtn.active {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .Looksbtn:hover {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .info-row{
    padding: 1px;
    margin-right: 50px;
    margin-top: -10px;
  }
  /*欄位通用設定*/
  .btn-right {
    text-align: right;
    margin-top: 10px;
  }
  .btn-right .el-icon {
    margin-left: -10px;  /* 控制圖標之間的間距 */
    margin-right: 10px;
    margin-top: 10px;
  }
  .diagnosis-input {
    margin-top: 10px; /* 與標籤和按鈕的間距 */
    border-radius: 10px; /* 使輸入框具有圓角 */
    background-color: #eeeeee; /* 使輸入框的背景顏色與圖片中的類似 */
    width: 100%; /* 使輸入框填滿行寬 */
    box-sizing: border-box; /* 確保 padding 和 border 不會影響寬度計算 */
  }
  /*Auxiliary Diagnostic Information*/
  .generate-button {
    margin-top: 4px;
    margin-left: -35px;
    background: linear-gradient(0.35turn,#B9C3F5, #DD73DF);
    color: #ffffff;
    border-color: #ffffff;
    border-radius: 16px;
    font-size: 10px; /* 調整文字大小 */
  }
  .generate-button.active {
    background: linear-gradient(0.35turn,#7179a3, #7e3d80);
    color: #464343;
    border-color: #464343;
  }
  .generate-button:hover {
    
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: #c5c5c5;
    border-color: #8f8f8f;
  }
  /*Prescription*/
  .new-medication-button{
    margin-left: -13px;
    background-color: #e0bcdd;
    color: #000000;
    border-color: #e0bcdd;
    border-radius: 16px;
  }
  .new-medication-button.active {
    background-color: #8a5f86;
    color: #50474f;
    border-color: #50474f;
  }
  .new-medication-button:hover {
    background-color: #aa79a6;
    color: #524350;
    border-color: #524350;
  }
  /*Final Diagnosis*/
  .copy-button {
    margin-left: -70px;
    background-color: #E8E7E0;
    color: #000000;
    border-color: #E8E7E0;
    border-radius: 16px;
  }
  .copy-button.active {
    background-color: #88867c;
    color: #757575;
    border-color: #757575;
  }
  .copy-button:hover {
    background-color: #bdbbb1;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }  
  .health-education-block {
    margin-left: 25px;
    margin-top: 20px;
    padding-right: 67px;
    background-color: pink;
    border-radius: 8px;
    width: auto; /* 保持自適應 */
  }
  /* 衛教圖片下載 */
  .GoDLHE {
    margin-left: -60px;
    background-color: #B098E2;
    color: #ffffff;
  }
  .GoDLHE.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .GoDLHE:hover {
    background-color: #947ec4;
    color: #dddddd;
  }
  .pink-button {
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: white; /* 按钮文字颜色 */
  }
  /* 圖片容器設定相對定位 */
  .image-container {
    position: relative;
    width: 100%; /* 根據需要調整寬度 */
    height: auto;
  }
  /* 圖片等比例縮放 */
  .responsive-image {
    width: 100%;
    height: auto;
  }
  /* 衛教標題文字 */
  .custom-text-Title {
    position: absolute;
    top: 40px; /* 根據需要調整文字的垂直位置 */
    left: 60px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 0px;
    white-space: pre-line;
    word-break: break-word;
    font-size: 17px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  /* 衛教內文文字 */
  .custom-text-Content {
    position: absolute;
    top: 80px; /* 根據需要調整文字的垂直位置 */
    left: 10px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 15px;
    white-space: pre-line; 
    word-break: break-word;
    font-size: 9px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  .pink-button:hover {
    background-color: #8f8f8f; /* 鼠标悬浮时的按钮颜色 */
  }
  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: contain; /* 圖片大小設置為等比例縮放 */
    background-repeat: no-repeat; /* 防止背景重複 */
  }
  }
  
  @media (min-width: 1024px){
    .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .header {
    display: flex;
  }
  .card {
    background-color: #eaf5fc;
    border-radius: 30px;
    padding: 15px;
    width: auto;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  }
  .LooksBlock {
    background-color: #F6FCF3; /* 背景顏色 */
    padding: 20px; /* 內邊距 */
    border-radius: 30px; /* 圓角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
    margin-bottom: 10px;
  }
  .EditBlock{
    background-color: #ffffff;
    border-radius: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 陰影效果 */
  }
  .form-block{
    padding: 10px;
  }
  /*上方查看列表CSS*/
  .section-title {
    display: block;
    margin-bottom: 10px; /* 與表格之間的間距 */
    margin-top: 20px; /* 與上方元素之間的間距 */
    font-weight: bold;
    font-size: 16px;
    color: #333;
  }
  .custom-table {
    background-color: #F6FCF3; /* 背景顏色 */
    border-radius: 10px; /* 圓角 */
  }
  .custom-table :deep(.el-table__header-wrapper),
  .custom-table :deep(.el-table__body-wrapper),
  .custom-table :deep(.el-table__header),
  .custom-table :deep(.el-table__body) {
    background-color: #F6FCF3; /* 背景顏色 */
  }
  .custom-table :deep(.el-table__header-wrapper th),
  .custom-table :deep(.el-table__body-wrapper td) {
    background-color: #F6FCF3; /* 背景顏色 */
    border-bottom: 1px solid #e0e0e0; /* 底部邊框 */
  }
  .Rx-table {
    border-radius: 6px; /* 圆角 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
    margin-top: 10px; /* 与上方元素的间距 */
  }
  .el-form-item {
    margin-left: 50px;
    right: 70%;
    margin-bottom: 20px;
    margin-top: 10px;
  }
  .el-button {
    margin-top: 6px;
    margin-left: 1%;
    margin-bottom: 15px;
  }
  .action-buttons {
    margin-left: 80%;
  }
  .back-button{
    margin-top: 15px;
  }
  .dialog-footer{
    margin-left: 85%;
  }
  .custom-form .compact-form-item {
    margin-bottom: 12px; /* 仅对特定表单项之间的距离进行调整 */
  }
  .custom-form .form-input {
    height: 38px; /* 仅对特定表单项中的输入框进行高度调整 */
  }
  /* Prescription line 分割線*/ 
  .divider {
    border: none;
    border-top: 1px solid #ccc; /* 线条的颜色和宽度 */
    margin: 20px 0; /* 上下的间距 */
  }
  .Looksbtn {
    color: #777777;
    border: 1px solid #F6FCF3;
    height: 32px;
    border-radius: 16px;
    padding: 0 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    background-color: #F6FCF3;
    cursor: pointer;
    font-size: 14px;
    text-decoration: none;
  }
  .Looksbtn.active {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .Looksbtn:hover {
    background-color: #D8EECA;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }
  .info-row{
    padding: 10px;
  }
  /*欄位通用設定*/
  .btn-right {
    text-align: right;
    margin-top: 10px;
  }
  .btn-right .el-icon {
    margin-left: 10px;  /* 控制圖標之間的間距 */
    margin-right: 10px;
    margin-top: 10px;
  }
  .diagnosis-input {
    margin-top: 10px; /* 與標籤和按鈕的間距 */
    border-radius: 10px; /* 使輸入框具有圓角 */
    background-color: #eeeeee; /* 使輸入框的背景顏色與圖片中的類似 */
    width: 100%; /* 使輸入框填滿行寬 */
    box-sizing: border-box; /* 確保 padding 和 border 不會影響寬度計算 */
  }
  /*Auxiliary Diagnostic Information*/
  .generate-button {
    background: linear-gradient(0.35turn,#B9C3F5, #DD73DF);
    color: #ffffff;
    border-color: #ffffff;
    border-radius: 16px;
  }
  .generate-button.active {
    background: linear-gradient(0.35turn,#7179a3, #7e3d80);
    color: #464343;
    border-color: #464343;
  }
  .generate-button:hover {
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: #c5c5c5;
    border-color: #8f8f8f;
  }
  /*Prescription*/
  .new-medication-button{
    background-color: #e0bcdd;
    color: #000000;
    border-color: #e0bcdd;
    border-radius: 16px;
  }
  .new-medication-button.active {
    background-color: #8a5f86;
    color: #50474f;
    border-color: #50474f;
  }
  .new-medication-button:hover {
    background-color: #aa79a6;
    color: #524350;
    border-color: #524350;
  }
  /*Final Diagnosis*/
  .copy-button {
    background-color: #E8E7E0;
    color: #000000;
    border-color: #E8E7E0;
    border-radius: 16px;
  }
  .copy-button.active {
    background-color: #88867c;
    color: #757575;
    border-color: #757575;
  }
  .copy-button:hover {
    background-color: #bdbbb1;
    color: #5e5e5e;
    border-color: #5e5e5e;
  }  
  .health-education-block {
    margin-left: 55px;
    margin-right: 0;
    margin-top: 20px;
    padding-right: 10px;
    background-color: pink;
    border-radius: 8px;
    width: auto; /* 保持自適應 */
  }
  /* 衛教圖片下載 */
  .GoDLHE {
    background-color: #B098E2;
    color: #ffffff;
  }
  .GoDLHE.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .GoDLHE:hover {
    background-color: #947ec4;
    color: #dddddd;
  }
  .pink-button {
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    background: linear-gradient(0.35turn,#98a2d4, #b658b8);
    color: white; /* 按钮文字颜色 */
  }
  /* 圖片容器設定相對定位 */
  .image-container {
    position: relative;
    width: 100%; /* 根據需要調整寬度 */
    height: auto;
  }
  /* 圖片等比例縮放 */
  .responsive-image {
    width: 100%;
    height: auto;
  }
  /* 衛教標題文字 */
  .custom-text-Title {
    position: absolute;
    top: 70px; /* 根據需要調整文字的垂直位置 */
    left: 150px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 5px;
    white-space: pre-line;
    word-break: break-word;
    font-size: 50px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  /* 衛教內文文字 */
  .custom-text-Content {
    position: absolute;
    top: 220px; /* 根據需要調整文字的垂直位置 */
    left: 10px; /* 根據需要調整文字的水平位置 */
    color: #000; /* 根據圖片調整字體顏色 */
    padding: 15px;
    white-space: pre-line; 
    word-break: break-word;
    font-size: 18.5px; /* 調整文字大小 */
    font-family: "Chocolate Classical Sans", sans-serif; /* 設定字型 */
    line-height: 1.25; /* 調整行距以提升閱讀性 */
  }
  .pink-button:hover {
    background-color: #8f8f8f; /* 鼠标悬浮时的按钮颜色 */
  }
  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: contain; /* 圖片大小設置為等比例縮放 */
    background-repeat: no-repeat; /* 防止背景重複 */
  }
  }

</style>
  