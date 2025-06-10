<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import {onBeforeMount, ref, watch, watchEffect} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

defineEmits([
  ...useDialogPluginComponent.emits
])


const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()
const $q = useQuasar()

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

const listData = ref([])

function getColorByStatus(status) {
  switch (status) {
    case 0:
      return ''
    case 1:
      return 'bg-blue-3'
    case 2:
      return 'bg-yellow-3'
    case 3:
      return 'bg-green-3'
    case 4:
      return 'bg-yellow-3'
  }
}

watchEffect(async () => {
  $q.loading.show({message: "Загрузка данных"})
  let r = await api.get(`/api/upload/${props.id}/get-programs/`)
  listData.value = _.orderBy(r.data, x => x.status, 'desc')
  $q.loading.hide()
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 900px; max-width: 80vw">
      <q-card-section class="text-h6">
        Список дисциплин и практик
      </q-card-section>

      <q-separator/>

      <q-card-section style="max-height: 80vh" class="scroll">
        <div class="q-gutter-y-sm">
          <q-field
            dense
            v-for="item in listData"
            outlined
            stack-label
            :label="item.status_verbose"
            :class="getColorByStatus(item.status)"
          >
            <template #control>
              <div class="text-subtitle1">
                {{ item.dis }}
                <q-btn flat icon="mdi-download" v-if="item.status == 3" :href="`/api/generator/${item.id}/get-rpd-report/`" target="_blank"/>
              </div>
            </template>
          </q-field>
        </div>
      </q-card-section>

      <q-separator/>

      <q-card-actions align="right">
        <q-btn flat label="Закрыть" @click="onDialogOK"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
