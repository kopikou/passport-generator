<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref, onBeforeMount} from "vue";
import _, {random} from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  disciplineLibrary,
} = storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const $q = useQuasar()
const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const correct = computed(() => {
  if (htppLink.value == '') return true
  if (bibDisc.value == '') return true
  if (yearIzd.value <= 0) return true

  return false
})

const htppLink = ref<string>('')
const bibDisc = ref<string>('')
const yearIzd = ref<number>()
const type = ref<number>(0)

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})
  console.log(disciplineLibrary.value[0])
  if (type.value == 0) {
    disciplineLibrary.value[0].value['dopBook'].push({
      id: Math.floor(Math.random() * 100000),
      http_link: htppLink.value,
      bib_disc: bibDisc.value,
      izd_type: yearIzd.value,
    })
  } else {
    disciplineLibrary.value[0].value['mainBook'].push({
      id: Math.floor(Math.random() * 100000),
      http_link: htppLink.value,
      bib_disc: bibDisc.value,
      izd_type: yearIzd.value,
    })
  }
  $q.loading.hide()
  onDialogOK()
}


</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-ma-md">
        <p>Библиографическая ссылка заполняется в соответствии с ГОСТ Р 7.0.5 2008</p>
        <div class="q-mt-md q-gutter-md">
          <q-input
            label="Библиографическая ссылка"
            v-model="bibDisc"
            stack-label
            filled
            type="textarea"
          />
          <q-input
            label="URL-Ссылка"
            v-model="htppLink"
            stack-label
            filled
          />
          <q-input
            label="Год издания"
            v-model="yearIzd"
            type="number"
            stack-label
            filled
          />
          <q-select
            label="Тип литературы"
            v-model="type"
            map-options
            emit-value
            filled
            option-value="value"
            option-label="name"
            :options="[{name: 'Основная', value: 1}, {name: 'Дополнительная', value: 0}]"
          />
        </div>
      </div>
      <q-card-actions align="right">
        <q-btn flat color="teal" label="Сохранить" @click="onOKClick" :disabled="correct"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
