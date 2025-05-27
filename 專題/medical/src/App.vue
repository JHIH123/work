<template>
  <div id="app" class="app-container">
    <Menu />
    <DeleteConfirmation />
    <div class="content">
      <router-view></router-view>
    </div>

    <div>
      
      <SearchWindow :visible="isSearchWindowVisible" @close="isSearchWindowVisible = false" @search="performSearch"/>
      <!-- 其他代碼 -->
    </div>
  </div>
</template>

<script>
import Menu from './components/Menu.vue';
import SearchWindow from './components/SearchWindow.vue';
import DeleteConfirmation from './components/DeleteConfirmation.vue';

export default {
  name: 'App',
  components: {
    Menu,
    SearchWindow,
    DeleteConfirmation,
  },
  data() {
    return {
      isSearchWindowVisible: false,
    };
  },
  methods: {
    showSearchWindow() {
      this.isSearchWindowVisible = true;
    },
    performSearch(searchCriteria) {
      console.log(searchCriteria);
      this.isSearchWindowVisible = false;
      // 根據searchCriteria進行搜尋操作
    }
  }
}
</script>

<style scoped>

/* 720~1024 */
@media (min-width: 720px){
  body, html, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  font-family: Arial, sans-serif;
}

.app-container {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
  margin-left: 230px; 
  overflow-y: auto;
  
} 

button {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1000;
}
}
/* 1024以下 */
@media (max-width: 1024px){
  body, html, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  font-family: Arial, sans-serif;
}

.app-container {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
  margin-left: 190px; 
  overflow-y: auto;
  
} 

button {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1000;
}
}
/* 1024以上 */
@media (min-width: 1024px){
  body, html, #app {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    font-family: Arial, sans-serif;
  }

  .app-container {
    display: flex;
  }

  .content {
    flex: 1;
    padding: 20px;
    margin-left: 230px; 
    overflow-y: auto;
    
  } 

  button {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 1000;
  }
}


</style>
