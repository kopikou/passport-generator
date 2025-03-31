<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import EmptyIcon from "components/EmptyIcon.vue";
import {api} from "boot/axios";

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()
const $q = useQuasar()


const generatorViewStore = useGeneratorViewStore();

const {
  oldPlans,
  activeRpdId,
} = storeToRefs(generatorViewStore)


async function copyProgram(id) {
  let r = await api.get(`/api/generator/${activeRpdId.value}/copy-old-rpd-program/`, {params: {old_pk: id}})
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">

      <q-card-section>
        <div class="text-h6">
          Копирование РПД
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section>
        <div class="text-subtitle1" v-if="oldPlans.length == 0">
          Нет программ подходящих для копирования :(
          <empty-icon/>
        </div>
        <div v-else class="q-gutter-sm">
          <q-field
            v-for="plan in oldPlans"
            outlined
            stack-label
            :label="plan.species"
          >
            <template #control>
              <div>
                {{ plan.abbrprofile }} - {{ String(plan.startyear).slice(-2) }}
              </div>
            </template>

            <template #append>
              <q-btn flat icon="mdi-clipboard-outline" color="black" @click="copyProgram(plan.id)"/>
            </template>
          </q-field>
        </div>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
<!--        <q-btn flat color="teal" label="Сохранить" @click="onOKClick"/>-->
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
