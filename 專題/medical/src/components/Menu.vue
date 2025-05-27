<template>
  <div class="sidebar">
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
    </div>
    <el-menu :default-active="activeMenuItem" class="el-menu" router @select="handleSelect">
      <div class="menu-top">
        <el-menu-item index="1" @click="$router.push('/')">
          <img src="@/assets/appointment.png" alt="Appointments" class="menu-icon" />
          <span slot="title">Appointments</span>
        </el-menu-item>
        <el-menu-item index="2" @click="$router.push('/patients')">
          <img src="@/assets/patient.png" alt="Patient" class="menu-icon" />
          <span slot="title">Patients</span>
        </el-menu-item>
        <el-menu-item index="3" @click="$router.push('/Inpatients')">
          <img src="@/assets/inpatient.png" alt="Inpatient" class="menu-icon" />
          <span slot="title">Inpatients</span>
        </el-menu-item>
        <el-menu-item index="4" @click="$router.push('/Statistics')">
          <img src="@/assets/Statistics.png" alt="Statistics" class="menu-icon" />
          <span slot="title">Statistics</span>
        </el-menu-item>
        <el-menu-item index="5" @click="$router.push('/Analysis')">
          <img src="@/assets/analysis.png" alt="Analysis" class="menu-icon" />
          <span slot="title">Analysis</span>
        </el-menu-item>
        
      </div>

      <div class="menu-bottom">
        <!-- <el-menu-item index="10" @click="$router.push('/Notifications')">
          <el-icon><Bell /></el-icon>
          <span slot="title">Notification</span>
        </el-menu-item>
        <el-menu-item index="11" @click="$router.push('/Settings')">
          <el-icon><Setting /></el-icon>
          <span slot="title">Setting</span>
        </el-menu-item> -->
        <el-menu-item index="12" @click="$router.push('/profile')">
          <img src="@/assets/doctor.jpg" alt="Profile" class="menu-icon" />
          <span slot="title">user</span>
        </el-menu-item>
      </div>
    </el-menu>
  </div>
</template>

<script>
  import { Document } from '@element-plus/icons-vue';
  
  export default {
    name: 'Menu',
    components: {
      Document,
    },
    data() {
      return {
        activeMenuItem: '1' // 默认激活的菜单项
      };
    },
    watch: {
      $route(to, from) {
        this.activeMenuItem = this.getMenuIndexFromRoute(to.path);
      }
    },
    created() {
      this.activeMenuItem = this.getMenuIndexFromRoute(this.$route.path);
    },
    methods: {
      getMenuIndexFromRoute(routePath) {
        switch(routePath) {
          case '/patients': return '2';
          case '/NewPatients': return '2';
          case '/Inpatients': return '3';
          case '/NewInpatient': return '3';
          case '/Statistics': return '4';
          case '/Analysis': return '5';

          case '/Notifications': return '6';
          case '/Settings': return '7';
          case '/profile': return '8';
          default: return '1';
        }
      },
      
    }
  };
</script>

<style scoped>


/* 720~1024 */
@media (min-width: 720px) {
  
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    height: 100vh;
    background-color: #ffffff;
    margin-left: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .menu-top {
    background-color: #eaf5fc; /* fafaFB */
    border-radius: 20px;
    margin-left: auto;
    height: 550px;
  }
  
  .menu-bottom {
    margin-top: 10%;
    background-color: #eaf5fc;
    border-radius: 20px;
    margin-left: auto;
  }
  
  .logo-container {
    display: flex;
    align-items: center;
    height: 80px;
    max-height: 60px;
  }
  
  .menu-icon {
    width: 24px; /* 你可以根據需要調整這個值 */
    height: 24px; /* 你可以根據需要調整這個值 */
    margin-right: 10px; /* 圖標和文字之間的間距 */
  }
  .logo {
    max-width: 100%;
    max-height: 100%;
    
  }
  
  .el-menu {
    position: fixed;
    margin-top: 50px; /* 菜单上方空间 */
    width: 200px;
    left: 0px;
    background-color: #ffffff;
    border-right: none; /* 移除右侧边框 */
  }

}
/* 1024以下 */
@media (max-width: 1024px) {
  .el-menu-item {
    border-radius: 20px; /* 增加這一行來確保選單項目也有圓角 */
  }
  .sidebar {
    position: fixed; /* 位置固定 */
    top: 5px;
    left: 0;
    width: 200px;
    background-color: #ffffff;
    margin-left: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    
  }

  .menu-top {
    margin-top: 10px;
    background-color: #eaf5fc; /* fafaFB */
    border-radius: 20px;
    margin-left: auto;
    height: 570px;
    font-size: 4px;
  }

  .menu-bottom {
    margin-top: 10%;
    background-color: #eaf5fc;
    border-radius: 20px;
    margin-left: auto;
  }

  .logo-container {
    display: flex;
    align-items: center;
    height: 80px;
    max-height: 50px;
    border-radius: 20px;
  }

  .menu-icon {
    width: 24px; /* 你可以根據需要調整這個值 */
    height: 24px; /* 你可以根據需要調整這個值 */
    margin-right: 10px; /* 圖標和文字之間的間距 */
  }
  .logo {
    max-width: 100%;
    max-height: 100%;
  }

  .el-menu {
    position: fixed;
    margin-top: 50px; /* 菜单上方空间 */
    width: 200px;
    left: 0px;
    background-color: #ffffff;
    border-right: none; /* 移除右侧边框 */
  }
}
/* 1024以上 */
@media (min-width: 1024px) {
  .sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  background-color: #ffffff;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu-top {
  margin-top: 5px;
  background-color: #eaf5fc; /* fafaFB */
  border-radius: 20px;
  margin-left: auto;
  height: 550px;
}

.menu-bottom {
  margin-top: 10%;
  background-color: #eaf5fc;
  border-radius: 20px;
  margin-left: auto;
}

.logo-container {
  display: flex;
  align-items: center;
  height: 70px;
  max-height: 60px;
}

.menu-icon {
  width: 24px; /* 你可以根據需要調整這個值 */
  height: 24px; /* 你可以根據需要調整這個值 */
  margin-right: 10px; /* 圖標和文字之間的間距 */
}
.logo {
  margin-top: 1px;
  max-width: 100%;
  max-height: 100%;
  
}

.el-menu {
  position: fixed;
  margin-top: 56px; /* 菜单上方空间 */
  width: 250px;
  left: 0px;
  background-color: #ffffff;
  border-right: none; /* 移除右侧边框 */
}
}




</style>
