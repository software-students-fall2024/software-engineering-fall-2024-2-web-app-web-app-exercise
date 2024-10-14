function showInstructions(workoutId) {
    const instructionGroups = document.querySelectorAll('.instruction-group');
    
    instructionGroups.forEach(group => {
      group.classList.add('hidden');
    });
    
    document.getElementById(workoutId).classList.remove('hidden');
  }
