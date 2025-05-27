<script setup lang="ts">


import {useDialogPluginComponent, useQuasar} from "quasar";
import {computed, ref, watch} from "vue";
import {api} from "boot/axios";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const $q = useQuasar()

const protocolNumber = ref($q.localStorage.getItem('rpd_protocolNumber'))
const protocolDate = ref($q.localStorage.getItem('rpd_protocolDate'))
const meeting = ref($q.localStorage.getItem('rpd_meeting') || "заседании кафедры")

const disabled = computed(() => {
  if (!protocolNumber.value) return true
  if (!protocolDate.value) return true
  if (!meeting.value) return true

  return false
})

async function onAcceptClick() {
  onDialogOK({
    date: protocolDate.value,
    number: protocolNumber.value,
    meeting: meeting.value,
  })
}

watch([meeting, protocolNumber, protocolDate], () => {
  $q.localStorage.set('rpd_meeting', meeting.value);
  $q.localStorage.set('rpd_protocolNumber', protocolNumber.value);
  $q.localStorage.set('rpd_protocolDate', protocolDate.value);
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 500px;">
      <q-card-section>
        <div class="text-h6">
          Утверждение РПД
        </div>
      </q-card-section>
      <q-card-section>
        <div class="q-gutter-md">
<!--          <q-select-->
<!--            v-model="userType"-->
<!--            label="Кто утвердил"-->
<!--            :options="userTypeOptions"-->
<!--            stack-label-->
<!--            map-options-->
<!--            emit-value-->
<!--            filled-->
<!--          />-->
          <q-input
            v-model="meeting"
            type="text"
            stack-label
            label="Утвердили на"
            filled
          />
          <q-input
            v-model="protocolNumber"
            type="text"
            stack-label
            label="Номер протокола"
            filled
          />
          <q-input
            v-model="protocolDate"
            type="date"
            stack-label
            label="Дата протокола"
            filled
          />
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat color="secondary" label="Утвердить" :disable="disabled" @click="onAcceptClick" v-close-popup/>
        <q-btn flat color="negative" label="Отмена" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
