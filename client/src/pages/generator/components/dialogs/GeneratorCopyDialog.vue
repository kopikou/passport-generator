<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import EmptyIcon from "components/EmptyIcon.vue";
import {api} from "boot/axios";
import {computed, ref} from "vue";
import GeneratorAcceptDialog from "pages/generator/components/dialogs/GeneratorAcceptDialog.vue";
import GeneratorCopyOptionsDialog from "pages/generator/components/dialogs/GeneratorCopyOptionsDialog.vue";
import {CopyOptions} from "src/types";

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()
const $q = useQuasar()


const generatorViewStore = useGeneratorViewStore();

const {
  oldPlans,
  newPlans,
  commonPlans,
  activeRpdId,
} = storeToRefs(generatorViewStore)

const typeTab = ref('old');

async function copyOldProgram(id: number) {
  $q.dialog({
    component: GeneratorCopyOptionsDialog
  }).onOk(async (options: CopyOptions) => {

    // console.log(options)
    // return

     $q.loading.show({
      message: "Копирую"
    })
    let r = await api.post(`/api/generator/${activeRpdId.value}/copy-old-rpd-program/`, options, {params: {old_pk: id}})

    if (r.status == 200) {
      $q.notify({
        message: "УРА копирование удалось :)",
        position: "top-right",
        color: "positive",
      })
      await generatorViewStore.getData()
    } else {
      $q.notify({
        message: "Ошибка копирования, напишите в поддержку о вашей проблеме :(",
        position: "top-right",
        color: "negative",
      })
    }
    $q.loading.hide()
    onDialogOK()
  })
}

async function copyNewProgram(id: number) {
  $q.loading.show({
    message: "Копирую"
  })
  let r = await api.post(`/api/generator/${activeRpdId.value}/copy-rpd-program/`, {from_pk: id})

  if (r.status == 200) {
    $q.notify({
      message: "УРА копирование удалось :)",
      position: "top-right",
      color: "positive",
    })
    await generatorViewStore.getData()
  } else {
    $q.notify({
      message: "Ошибка копирования, напишите в поддержку о вашей проблеме",
      position: "top-right",
      color: "negative",
    })
  }
  $q.loading.hide()
  onDialogOK()
}


const textFilter = ref("");

const oldPlansFiltered = computed(() => {
  return oldPlans.value.filter(x => {
    return !textFilter.value
      || x.species.toLowerCase().includes(textFilter.value)
      || x.abbrprofile.toLowerCase().includes(textFilter.value)
  })
})
const newPlansFiltered = computed(() => {
  return newPlans.value.filter(x => {
    return !textFilter.value
      || x.species.toLowerCase().includes(textFilter.value)
      || x.abbrprofile.toLowerCase().includes(textFilter.value)
  })
})
const commonPlansFiltered = computed(() => {
  return commonPlans.value.filter(x => {
    return !textFilter.value
      || x.species.toLowerCase().includes(textFilter.value)
      || x.abbrprofile.toLowerCase().includes(textFilter.value)
  })
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <q-card-section>
        <div class="text-h6">
          Копирование данных из другого РПД
        </div>
      </q-card-section>
      <q-separator/>

      <div class="bg-primary rounded-borders">
        <div class="text-subtitle1 text-white q-px-md q-py-sm">
          Все данные об индикаторах и содержании тем дисциплины в текущей программе будут перезаписаны
        </div>
      </div>

      <q-card-section>
        <q-tabs
          v-model="typeTab"
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="old" label="Из старого генератора"/>
          <q-tab name="new" label="Из новых программ"/>
          <q-tab name="common" label="Из общих"/>
        </q-tabs>
      </q-card-section>
      <q-card-section>
        <q-input label="Поиск" v-model="textFilter"></q-input>
      </q-card-section>
      <q-card-section style="height: 50vh; overflow-y: auto">
        <q-tab-panels v-model="typeTab" animated>
          <q-tab-panel name="old">
            <q-field
              v-for="plan in oldPlansFiltered"
              outlined
              stack-label
              :label="plan.species"
            >
              <template #control>
                <div>
                  {{ plan.abbrprofile }}-{{ String(plan.startyear).slice(-2) }}
                </div>
              </template>

              <template #append>
                <q-btn label="скопировать" flat icon="mdi-clipboard-outline" color="black"
                       @click="copyOldProgram(plan.id)"/>
              </template>
            </q-field>
          </q-tab-panel>

          <q-tab-panel name="new">
            <q-field
              v-for="plan in newPlansFiltered.filter(x => x.id != activeRpdId)"
              outlined
              stack-label
              :label="plan.species"
            >
              <template #control>
                <div>
                  {{ plan.abbrprofile }}-{{ String(plan.startyear).slice(-2) }}
                </div>
              </template>

              <template #append>
                <q-btn label="скопировать" flat icon="mdi-clipboard-outline" color="black"
                       @click="copyNewProgram(plan.id)"/>
              </template>
            </q-field>
          </q-tab-panel>

          <q-tab-panel name="common">
            <q-field
              v-for="plan in commonPlansFiltered.filter(x => x.id != activeRpdId)"
              outlined
              stack-label
              :label="plan.species"
            >
              <template #control>
                <div>
                  {{ plan.abbrprofile }}-{{ String(plan.startyear).slice(-2) }}
                </div>
              </template>

              <template #append>
                <q-btn label="скопировать" flat icon="mdi-clipboard-outline" color="black"
                       @click="copyNewProgram(plan.id)"/>
              </template>
            </q-field>
          </q-tab-panel>

        </q-tab-panels>
      </q-card-section>
      <q-separator/>
      <q-card-actions align="right">
        <!--        <q-btn flat color="teal" label="Сохранить" @click="onOKClick"/>-->
        <q-btn flat color="red" label="Закрыть" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
