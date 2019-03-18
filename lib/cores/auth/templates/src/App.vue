<template>
  <v-app light>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>

            <v-card class="elevation-12">
              <v-toolbar dark color="grey darken-1">
                <v-toolbar-title> 登入</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>

              <v-form method="post"
                      action="">
                <v-card-text>
                  <v-text-field
                          color="brown lighten-1"
                          prepend-icon="person"
                          name="username"
                          label="请输入用户名"
                          type="text"
                          v-model="usr"
                  ></v-text-field>
                  <v-text-field
                          color="brown lighten-1"
                          prepend-icon="lock"
                          name="password"
                          label="请输入密码"
                          type="password"
                          v-model="pwd"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="grey lighten-2" type="submit" tabindex="0"
                         @keyup.enter="submit"> Go
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>

          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  export default {
    name: 'Auth',
    data() {
      return {
        usr: "admin",
        pwd: "admin",
      }
    }
  }
</script>
