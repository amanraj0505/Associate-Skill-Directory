var data = [
        { skill: 'C++', Code: 'C++' },
        { skill: 'Java', Code: 'java' },
        { skill: 'cloud', Code: 'cloud' },
        { skill: 'Python', Code: 'python' },
        { skill: 'Web', Code: 'web' },
        { skill: 'Javascript', Code: 'javascript' },
        { skill: 'Android', Code: 'android' },
        { skill: 'ML', Code: 'ML' },
        { skill: 'ADA', Code: 'algorithms' },
        { skill: 'API', Code: 'api' },
        { skill: 'Linux', Code: 'Linux' },
        { skill: 'Shell', Code: 'Shell' },
        { skill: 'git', Code: 'git' },
        { skill: 'SQL', Code: 'SQL' },
        { skill: 'Problem-solving', Code: 'Problem-solving'},
        { skill: 'Kubernetes', Code: 'Kubernetes' },
        { skill: 'Azure-Fundamentals', Code: 'Azure-Fundamentals' },
        { skill: 'Azure-Admin', Code: 'Azure-Admin' },
        { skill: 'Azure-developer', Code: 'Azure-developer' },
        { skill: 'Azure-Architect', Code: 'Azure-Architect' },
        { skill: 'AWS-Foundation', Code: 'AWS-Foundation' },
        { skill: 'AWS-Associate', Code: 'AWS-Associate' },
        { skill: 'AWS-Professional', Code: 'AWS-professional' },
        { skill: 'AWS-Specility', Code: 'AWS-Specility' },
        { skill: 'Containers', Code: 'Containers' },
        { skill: 'Team-Building', Code: 'Team-Building' },
        { skill: 'Management', Code: 'Management' },
        { skill: 'Communication', Code: 'Communication' },
        { skill: 'Teamwork', Code: 'Teamwork' },
        { skill: 'Critical-Thinking', Code: 'Critical-Thinking' },
        { skill: 'Adaptability', Code: 'Adaptability' },
        { skill: 'Conflict-management', Code: 'Conflict-management' },
        { skill: 'Leadership', Code: 'Leadership' },
        { skill: 'Creativity', Code: 'Creativity' },
        { skill: 'Stress-management', Code: 'Stress-management' }
		];
 // initialize MultiSelect component
    var skillSet = new ej.dropdowns.MultiSelect({
        // set the colors data to dataSource property
        dataSource: data,
        // map the appropriate columns to fields property
        fields: { text: 'skill', value: 'Code' },
        // set the value to MultiSelect
        value: [],
        // set the placeholder to MultiSelect input element
        placeholder: 'SELECT SKILLS',
        // set the type of mode for how to visualized the selected items in input element.
        mode: 'Box',
        // bind the tagging event
        tagging: function (e) {
            // set the current selected item text as class to chip element.
            e.setClass(e.itemData[skillSet.fields.text].toLowerCase());
        }
    });
    console.log(skillSet)
	// render initialized multiSelect
    skillSet.appendTo('#select');
