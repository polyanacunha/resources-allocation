import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-data-entry',
  templateUrl: './data-entry.component.html',
  styleUrls: ['./data-entry.component.css']
})
export class DataEntryComponent {
  dataForm!: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService) {
    this.createForm();
  }
  createForm() {
        this.dataForm = this.fb.group({
      professor: this.fb.group({
        nome: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]]
      }),
      disciplina: this.fb.group({
        nome: ['', Validators.required],
        cargaHorariaSemanal: ['', Validators.required]
      }),
      turma: this.fb.group({
        semestre: ['', Validators.required],
        periodo: ['', Validators.required]
      }),
      curso: this.fb.group({
        nome: ['', Validators.required]
      }),
      disponibilidade: this.fb.group({
        dia: ['', Validators.required],
        periodo: ['', Validators.required]
      }),
      relacaoDisciplinaProfessor: this.fb.group({
        professorId: ['', Validators.required],
        disciplinaId: ['', Validators.required]
      }),
      cursoDisciplina: this.fb.group({
        cursoId: ['', Validators.required],
        disciplinaId: ['', Validators.required],
        semestre: ['', Validators.required]
      })
    });
  }

  onSubmit() {
    if (this.dataForm.valid) {
      this.apiService.submitData(this.dataForm.value).subscribe(
        response => {
          console.log('Dados enviados com sucesso', response);
          alert('Dados enviados com sucesso!');
        },
        error => {
          console.error('Erro ao enviar dados', error);
          alert('Erro ao enviar dados!');
        }
      );
    } else {
      alert('Por favor, preencha todos os campos necessários.');
    }
  }
}


// import { Component, OnInit } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { ApiService } from '../api.service';

// @Component({
//   selector: 'app-data-entry',
//   templateUrl: './data-entry.component.html',
//   styleUrls: ['./data-entry.component.css']
// })
// export class DataEntryComponent implements OnInit {
//   dataForm!: FormGroup;

//   constructor(private fb: FormBuilder, private apiService: ApiService) {}
//   ngOnInit(): void {
//     this.dataForm = this.fb.group({
//       professor: this.fb.group({
//         nome: ['', Validators.required],
//         email: ['', [Validators.required, Validators.email]]
//       }),
//       disciplina: this.fb.group({
//         nome: ['', Validators.required],
//         cargaHorariaSemanal: ['', Validators.required]
//       }),
//       turma: this.fb.group({
//         semestre: ['', Validators.required],
//         periodo: ['', Validators.required]
//       }),
//       curso: this.fb.group({
//         nome: ['', Validators.required]
//       }),
//       disponibilidade: this.fb.group({
//         dia: ['', Validators.required],
//         periodo: ['', Validators.required]
//       }),
//       relacaoDisciplinaProfessor: this.fb.group({
//         professorId: ['', Validators.required],
//         disciplinaId: ['', Validators.required]
//       }),
//       cursoDisciplina: this.fb.group({
//         cursoId: ['', Validators.required],
//         disciplinaId: ['', Validators.required],
//         semestre: ['', Validators.required]
//       })
//     });
//   }

//   onSubmit() {
//     if (this.dataForm.valid) {
//       this.apiService.submitData(this.dataForm.value).subscribe(
//         response => {
//           console.log('Dados enviados com sucesso', response);
//           alert('Dados enviados com sucesso!');
//         },
//         error => {
//           console.error('Erro ao enviar dados', error);
//           alert('Erro ao enviar dados!');
//         }
//       );
//     } else {
//       alert('Por favor, preencha todos os campos necessários.');
//     }
//   }
// }
