<script setup lang="ts">

import {onBeforeMount, ref} from "vue";
import {useQuasar} from "quasar";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";

const mainStore = useMainStore();
const {csrf} = storeToRefs(mainStore)
const files = ref([])

const $q = useQuasar()

async function getFiles() {
  $q.loading.show()
  let r = await api.get("/api/upload/get-files/")
  files.value = r.data.items
  $q.loading.hide()
}

function removeFile(file_id) {
  $q.dialog({
    title: 'Удаление файла',
    message: 'Вы точно хотите отправить файл в архив?',
    ok: {
      label: 'В архив',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {
    let r = await api.delete("/api/upload/remove-files/", {headers: {'X-CSRFToken': csrf.value}, data: {id: file_id}})
    if (!r.data.success) {
      $q.notify({
        type: 'negative',
        message: `Не получилось удалить файл, попробуйте позже :(`,
      })
    } else {
      $q.notify({
        type: 'secondary',
        message: `Файл удален :)  `,
      })
      let i = files.value.map(item => item.id).indexOf(file_id) // find index of your object
      files.value.splice(i, 1) // remove it from array
    }
  })

}

onBeforeMount(() => {
  getFiles()
})

</script>

<template>
  <div class="q-pa-lg">
    <q-list bordered class="rounded-borders" style="max-width: 1000px">
      <q-item-label header class="text-h6 text-black">Загруженные планы</q-item-label>
      <div v-for="file in files">
        <q-item>
          <q-item-section top class="col-6 gt-sm">
            <q-item-label class="q-mt-sm">{{ file.title }}</q-item-label>
          </q-item-section>

          <q-item-section top class="qt-sm">
            <q-item-label class="q-mt-sm text-grey-8">{{ file.status }}</q-item-label>
          </q-item-section>

          <q-item-section top side>
            <div class="q-gutter-xs">
              <q-btn class="gt-xs" flat dense round icon="mdi-magnify"
                     color="green" :to='`/view/${file.id}`'/>
              <q-btn :disable="file.status == 'Проверен'" class="gt-xs" flat dense round icon="mdi-delete" color="red"
                     @click="removeFile(file.id)"/>
            </div>
          </q-item-section>
        </q-item>
      </div>
    </q-list>
  </div>
</template>

<style scoped>

</style>
