<template>
  <router-view/>
</template>

<style>
@import"https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,400;1,700&display=swap";@import"https://fonts.googleapis.com/icon?family=Material+Icons";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: #ebebeb;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#flex{
    display: -webkit-flex;
    display: -moz-flex;
    display: -ms-flex;
    display: -o-flex;
    display: flex;
}

/* va-card スタイル*/
.cardContent {
  overflow: hidden;
  height: 50px;
  max-height: 50px;
  text-overflow: ellipsis;
}

.header { 
  grid-area: header;
  /*position: fixed; ヘッダーを固定する */
  max-height: 100px;
  width: 100%; /* ヘッダーの横幅を指定する */
}
.menu {
  grid-area: menu;
  max-height: 800px;
  max-width: min-content;
  min-width: min-content;
  overflow: auto;
}
.body {
  grid-area: body;
  max-height: 800px;
  width: auto;
  overflow: auto;
}
.footer { 
  grid-area: footer;
  padding: 20px;
  background-image:url("https://picsum.photos/1600/1200");
  background-repeat: no-repeat;
  background-position: center;
  background-color:rgba(255,255,255,0.6);
  background-blend-mode:lighten;
}

.loginForm{
  height: 150px;
  width: 300px;
}

.grid-container {
  display: grid;
  grid-template-areas:
    'header header header header header'
    'menu body body body body'
    'footer footer footer footer footer';
  gap: 10px;
  /*background-color: #2196F3;*/
  /*padding: 10px;*/
}

.grid-container > div {
  background-color: rgba(255, 255, 255, 0.8);
  text-align: center;
}
</style>
